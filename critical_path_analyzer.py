try:
    import pandas as pd
    import os
    from graphviz import Digraph
    import textwrap
    import argparse
    import itertools
except:
    import os
    os.system('pip install -r ./requirements.txt')
    import pandas as pd
    from graphviz import Digraph
    import textwrap
    import argparse
    import itertools

class critical_path_analyzer():
    def __init__(self, **kwargs):
        file = kwargs.get('file', 'bicycle_data.csv')
        csv_path = kwargs.get('csv_path', os.path.join(os.getcwd(), file))
        self.tasks = pd.read_csv(csv_path)
        self.tasks['Predecessors'] = self.tasks['Predecessors'].fillna(value='None')
        self.tasks['expected_value'] = (self.tasks['Most Likely'] * 4 + self.tasks['Optimistic'] + self.tasks[
            'Pessimistic']) / 6
        self.output_file_type = kwargs.get('output_file_type', 'png')
        if self.output_file_type is None:
            self.output_file_type = 'png'

        self.name = kwargs.get('name', 'initial')
        self.task_duration_col = kwargs.get('task_duration_col', 'expected_value')
        if self.task_duration_col is None:
            self.task_duration_col = 'expected_value'

        self.all_paths = [[]]
        self.critical_path = []
        self.get_critical_path()
        self.dot = self.make_graph()
        self.tasks.to_csv(f'{self.name}.csv')

        print(f"critical path is: {self.critical_path}")
        print(f"critical path based on {self.task_duration_col} is {round(self.critical_path_val,1)}")

    def wrap_text(self, text, length=20):
        wrapper = textwrap.TextWrapper(width=length)
        word_list = wrapper.wrap(text=text)
        return '\n'.join(word_list)

    def flatten(self, list):
        flat_list = []
        for sublist in list:
            for item in sublist.split(','):
                flat_list.append(item)
        return flat_list

    def make_graph(self):
        tasks, name, task_duration_col = self.tasks, self.name, self.task_duration_col

        file_name = os.path.join(os.getcwd(), f'{name}.gv')

        dot = Digraph(format=self.output_file_type)
        dot.attr(rankdir='LR')
        edges = []
        for i, r in tasks.iterrows():
            task_name = r['Activity Tasks'] + '\n'
            task_name += self.wrap_text(r['Task Name'], 20)
            task_name += f"\n {round(r[self.task_duration_col], 1)}"
            if r['critical_task']:
                dot.attr('node', shape='ellipse', style='filled', fillcolor='blue', fontcolor='white')
            else:
                dot.attr('node', shape='ellipse', style='filled', fillcolor='yellow', fontcolor='black')

            dot.node(r['Activity Tasks'], task_name)
            if r['Predecessors'] != 'None':
                for pred in r['Predecessors'].split(','):
                    edges.append(pred + r['Activity Tasks'])
        dot.edges(edges)
        dot.render(file_name)
        return dot

    def sum_path(self, path_list):
        task_df = self.tasks
        # print(self.task_duration_col)
        df = task_df[task_df['Activity Tasks'].isin(path_list)]
        try:
            return df[self.task_duration_col].sum()
        except Exception as e:
            print(df.columns)
            raise Exception(e)

    def depthFirst(self, graph, currentVertex, visited):
        visited.append(currentVertex)
        # print(graph[currentVertex])
        for vertex in graph[currentVertex]:
            if vertex not in visited:
               self.depthFirst(graph, vertex, visited.copy())
        self.all_paths.append(visited)
        # pulled form https://stackoverflow.com/questions/62656477/python-get-all-paths-from-graph

    def get_critical_path(self):
        graph = self.tasks[['Activity Tasks', 'Predecessors']]
        graph_d = {}
        for i, r in graph.iterrows():
            graph_d[r['Activity Tasks']] = r['Predecessors'].split(',') if r['Predecessors'] != 'None' else []
        # print(graph_d)
        self.depthFirst(graph_d, 'T', self.all_paths)
        self.critical_path_val = 0
        for i, path in enumerate(self.all_paths):
            if 'A' not in path:
                continue
            path = [p for p in path if p != []]

            val = self.sum_path(path)
            if val > self.critical_path_val:
                self.critical_path_val = val
                self.critical_path = path

        self.tasks['critical_task'] = self.tasks['Activity Tasks'].isin(self.critical_path)
        return self.critical_path


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("-file", "--file", help='file name in directory')
    parser.add_argument("-name", "--name", help='name for output files')
    parser.add_argument("-task_duration_col", "--task_duration_col", help='col to use for duration. default is calculated expected value')

    args = vars(parser.parse_args())
    critical_path_analyzer(**args)

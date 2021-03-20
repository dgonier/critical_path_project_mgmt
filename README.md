## Columbia Project Management course 3/20/21


### Example command

## dont wanna deal with environments?

Make sure to add or modify the csv files to colab in order to see changes

[Open in Colab](https://colab.research.google.com/github/dgonier/critical_path_project_mgmt/blob/master/critical_path_notebook.ipynb)

You can change the arguments in the second to last cell

to run everything go to runtime run all or hit ctrl f9

## arguments
* ``-file <file>`` argument is the csv file with the data you want to process. put the file in your directory
* ``-name <name>`` argument is the name you want to use for output files
* ``-task_duration_col <task_duration_col>`` argument is the column you want to use for calculating critical path times

```python critical_path_analyzer.py -file bicycle_data.csv -name optimistic -task_duration_col Optimistic```

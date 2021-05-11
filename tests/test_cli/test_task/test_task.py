from pike.task import Task


def test_from_callable():
    def task_callable():
        pass

    task = Task.from_callable(task_callable)
    assert task.name == "task-callable"
    assert task.method == task_callable


def test_reads_docstring():
    def task_callable():
        """
        The content of the task
        """
        pass

    task = Task.from_callable(task_callable)
    assert task.name == "task-callable"
    assert task.method == task_callable
    assert task.description == "The content of the task"


def test_parameters():
    def task_callable(arg1: str = "a default"):
        """
        Description

        :param arg1: The first argument
        """
        pass

    task = Task.from_callable(task_callable)
    assert task.description == "Description"
    assert len(task.parameters) == 1
    arg = task.parameters[0]
    assert arg.name == "arg1"
    assert arg.param_type == str
    assert arg.default == "a default"
    assert arg.description == "The first argument"
    assert arg.has_default
    assert not arg.is_var_positional

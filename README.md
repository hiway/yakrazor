# Yakrazor

Yak Razor: Scheduler for Yak Shavers

Do you find yourself starting a task,
only to find yourself on a side quest of a side quest that was 
a required diversion to complete the initial task?
But you've lost track of what prompted you 
to take up the side quest and now the original task
remains unfinished and you've moved on to something else.

## What is Yakrazor?

At version 0.1, Yakrazor is a dead simple ToDo list 
that is designed to assist in keeping track of 
what you were doing before you had to move your attention to something else.

### Screenshot

![Screenshot 2024-03-17 at 13-40-00 Yakrazor](https://github.com/hiway/yakrazor/assets/23116/27f9fe6e-6b87-470c-b434-7e4f011d6b1d)

## How do I use it?

The list of tasks is treated like a stack, 
you add new tasks at the top.
Every time you need to shift your attention to something,
make a note of what you're about to do.
You may find yourself several tasks deep and 
need to backtrack to the original task that set you off on this side quest.
Mark each tangent task off as completed and 
the top task will be what you were doing before.

If something else comes up that needs to be done later, 
press Shift+Enter to put it at the bottom of the todo list.


User interactions:

- Type what you need to get done and press Enter
  - You can use voice input on phone etc.
  - Tasks are added to top of todo list
  - Add a task to bottom of todo list by holding Shift while you press Enter
- Tap or click on the empty checkbox on left of a task to mark it done
  - Completed tasks are moved below pending tasks
- Tap on a completed task's checkbox if you realise it needs more work
  - Removing the done check moves task to top of the todo list
- Tap on the three vertical dots on right of the task name for more actions
  - Edit task name
  - Move task up or down in the list
  - Move task to top or bottom of list
  - Delete task


## Install

Currently Yakrazor is available as source distribution via Github,
it will be available to install via Python's `pip` or `pipx` utilities soon.


Using [poetry](https://python-poetry.org/docs/):

```console
git clone https://github.com/hiway/yakrazor.git
cd yakrazor
poetry install

poetry run yakrazor
```


Using Python's `venv`

```console
git clone https://github.com/hiway/yakrazor.git
cd yakrazor

python3.11 -m venv .venv
source .venv/bin/activate
pip install -e .

yakrazor
```

You'll need to remember to `source .venv/bin/activate` every time.


## Accessing from multiple devices

I personally use and recommend [Tailscale](https://tailscale.com).
Yakrazor will be available via your machine's Tailscale internal IP,
or even with its hostname on your phone once you have Tailscale set up
on both devices.


## Feedback and Contributing

Use Github's [Disussions](https://github.com/hiway/yakrazor/discussions/new/choose) 
for general topics and [Issues](https://github.com/hiway/yakrazor/issues) for bug reports.

While this is a personal project to scratch my own itch, 
I welcome contributions that improve the user experience,
fix bugs or add meaningful features. 

Please [disuss](https://github.com/hiway/yakrazor/discussions/new/choose)
what you plan to contribute if it is beyond a few lines of code
to save your and my time and efforts!

I'll be adopting a Code of Conduct for this project soon,
if the mere mention of this makes you not want to contribute, great!

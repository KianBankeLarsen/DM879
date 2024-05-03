AI Poker Bot
===

## 👋 Introduction
This is a mandatory project in DM879, Artificial Intelligence. The project explores how to develop a Poker bot using adversarial search strategies like stochastic Minimax with alpha-beta pruning. We have decided to fork the [MIT Poker Engine](https://github.com/mitpokerbots/engine) because our goal is the AI strategy and not the engine itself.

## 👷‍♂️ Getting Started
Visual Studio Code tasks has been configured to make building and project execution easier. In this context, we utilize Docker to ensure environment consistency by using a base image with the correct Python version and Python packages installed.

The task `run` builds and executes the project as it depends on `build`. The tasks are primarily partitioned due to cosmetic reasons. The `run` task is therefore often the preferred choice, since Docker only rebuilds the `poker` image if files have been changed in the meantime.

**`.vscode/tasks.json`**
```bash
{
    "tasks": [
        {
            "label": "build",
            "type": "shell",
            "group": "build",
            "command": "docker build . -t poker"
        },
        {
            "label": "run",
            "type": "shell",
            "group": "build",
            "dependsOn": ["build"],
            "command": "docker run -v ./logs/gamelog.log:/poker/gamelog.txt -v ./logs/A.log:/poker/A.txt -v ./logs/B.log:/poker/B.txt poker"
        }
    ]
}
```

Python packages must be specified in `requirements.txt`.
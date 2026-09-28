## Numbered Steps

### Step 1: Open the Command Prompt

1. Click the **Start** button.
2. Type `cmd`.
3. Click **Command Prompt**.

A black window opens with a line such as `C:\Users\YourName>`. This window is the Command Prompt.

### Step 2: Confirm That Git and Python Are Installed

1. Type the following command and press **Enter**:
   ```
   git --version
   ```
2. Type the following command and press **Enter**:
   ```
   py --version
   ```

Each command should display a version number, such as `git version 2.47.0.windows.1` or `Python 3.13.0`.

### Step 3: Install the Game's Display Tool

Windows needs one small add-on for the game to display in the Command Prompt. Type the following command and press **Enter**:

```
py -m pip install windows-curses
```

Wait until the line `Successfully installed windows-curses` appears.

### Step 4: Move to Your User Folder

Type the following command and press **Enter**:

```
cd %USERPROFILE%
```

### Step 5: Download (Clone) the Program

Type the following command and press **Enter**:

```
git clone https://github.com/trevorwattles/wrtg-316-instructions.git
```

Wait until the line `Receiving objects: 100%` appears and the cursor returns.

### Step 6: Open the Program's Folder

Type the following command and press **Enter**:

```
cd wrtg-316-instructions
```

### Step 7: Confirm That the Game File Is Present

Type the following command and press **Enter**:

```
dir
```

The file `dino.py` should appear in the list.

### Step 8: Maximize the Window

Click the **Maximize** button (the square in the upper-right corner of the window). The game needs space to display correctly.

### Step 9: Run the Game

Type the following command and press **Enter**:

```
py dino.py
```

The dinosaur game appears in the Command Prompt window.

### Step 10: Play the Game

Use the following keys to play:

| Key                               | Action |
| --------------------------------- | ------ |
| **Space**, **W**, or **Up Arrow** | Jump   |
| **S** or **Down Arrow**           | Duck   |
| **P**                             | Pause  |

### Step 11: Quit the Game

Press **Q** to quit. The normal Command Prompt window returns.

---

## Troubleshooting

| Problem                                                                  | Solution                                                                                                                                                                                                               |
| ------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `is not recognized as an internal or external command` appears in Step 2 | Close and reopen the Command Prompt, then try again. If the error remains, install Git from **git-scm.com** and Python from **python.org**. In the Python installer, check the box labeled **Add python.exe to PATH**. |
| Typing `python` opens the Microsoft Store                                | Type `py` instead of `python`, as shown in these instructions.                                                                                                                                                         |
| `No module named '_curses'` appears in Step 9                            | The add-on is missing. Repeat Step 3.                                                                                                                                                                                  |
| `destination path ... already exists` appears in Step 5                  | The program is already downloaded. Continue to Step 6.                                                                                                                                                                 |
| `No such file or directory` appears in Step 9                            | You are in the wrong folder. Repeat Step 6.                                                                                                                                                                            |
| The game looks cut off or garbled                                        | Maximize the window (Step 8) and run the game again.                                                                                                                                                                   |
| The keys do nothing                                                      | Click inside the Command Prompt window, then try again.                                                                                                                                                                |
| The Command Prompt stops responding                                      | Press **Ctrl + C** to stop the current command.                                                                                                                                                                        |

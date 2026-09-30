## Numbered Steps

### Step 1: Open the Terminal

Press **Ctrl + Alt + T**.

A window opens with a line of text that ends in `$`. This window is the terminal.

> **Troubleshooting**
>
> **Ctrl + Alt + T does not open the terminal.** Open the applications menu, search for **Terminal**, and click it.

### Step 2: Confirm That Git and Python Are Installed

1. Type the following command and press **Enter**:

   ```
   git --version
   ```

2. Type the following command and press **Enter**:

   ```
   python3 --version
   ```

Each command should display a version number, such as `git version 2.43.0` or `Python 3.12.3`.

> **Troubleshooting**
>
> **`command not found` appears.** Git or Python is not installed. Type `sudo apt install -y git python3` (on Fedora, `sudo dnf install -y git python3`), press **Enter**, and enter your computer password when asked.

### Step 3: Move to Your Home Folder

Type the following command and press **Enter**:

```
cd ~
```

### Step 4: Download (Clone) the Program

Type the following command and press **Enter**:

```
git clone https://github.com/trevorwattles/wrtg-316-instructions.git
```

Wait until the line `Receiving objects: 100%` appears and the cursor returns.

> **Troubleshooting**
>
> **`destination path ... already exists` appears.** The program is already downloaded. Continue to Step 5.

### Step 5: Open the Program's Folder

Type the following command and press **Enter**:

```
cd wrtg-316-instructions
```

### Step 6: Confirm That the Game File Is Present

Type the following command and press **Enter**:

```
ls
```

The file `dino.py` should appear in the list.

### Step 7: Maximize the Terminal Window

Double-click the title bar at the top of the terminal window to maximize it. The game needs space to display correctly.

### Step 8: Run the Game

Type the following command and press **Enter**:

```
python3 dino.py
```

The dinosaur game appears in the terminal window.

> **Troubleshooting**
>
> **`No such file or directory` appears.** You are in the wrong folder. Repeat Step 5.
>
> **The game looks cut off or garbled.** Maximize the window (Step 7) and run the game again.

### Step 9: Play the Game

Press **Space** to start. Use the following keys to play:

| Key                               | Action |
| --------------------------------- | ------ |
| **Space**, **W**, or **Up Arrow** | Jump   |
| **S** or **Down Arrow**           | Duck   |
| **P**                             | Pause  |

Press **Q** to quit when you are done playing. The normal terminal window returns.

> **Troubleshooting**
>
> **The keys do nothing.** Click inside the terminal window, then try again.

---

## General Troubleshooting

These problems can happen during any step.

| Problem                       | Solution                                        |
| ----------------------------- | ----------------------------------------------- |
| The terminal stops responding | Press **Ctrl + C** to stop the current command. |

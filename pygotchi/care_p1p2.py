import numpy as np
import time
import random

### Utilities

def top_right(tama):
    return tama.Matrix()[0:8, 24:32]

def bottom_right(tama):
    return tama.Matrix()[8:16, 24:32]

def bottom_left(tama):
    return tama.Matrix()[8:16, 0:8]

### Images

skull = np.array([
    [0,0,0,0,0,0,0,0],
    [0,0,1,1,1,1,1,0],
    [0,1,1,1,1,1,1,1],
    [0,1,0,0,1,0,0,1],
    [0,1,1,1,1,1,1,1],
    [0,1,1,1,0,1,1,1],
    [0,0,1,1,1,1,1,0],
    [0,0,1,0,1,0,1,0],
])

heart = np.array([
    [0,0,0,0,0,0,0,0],
    [0,1,1,0,1,1,0,0],
    [1,0,0,1,0,0,1,0],
    [1,0,0,0,0,0,1,0],
    [1,0,0,0,0,0,1,0],
    [0,1,0,0,0,1,0,0],
    [0,0,1,0,1,0,0,0],
    [0,0,0,1,0,0,0,0],
])

poop1 = np.array([
    [1,0,0,0,0,0,0,0],
    [0,1,0,0,0,0,1,0],
    [1,0,0,0,0,0,0,1],
    [0,0,0,1,0,0,1,0],
    [0,0,0,1,1,0,0,0],
    [0,0,1,1,0,1,0,0],
    [0,1,0,1,1,1,1,0],
    [0,1,1,1,1,1,1,0],
])

poop2 = np.array([
    [0,0,0,0,0,0,0,1],
    [0,1,0,0,0,0,1,0],
    [1,0,0,0,0,0,0,1],
    [0,1,0,1,0,0,0,0],
    [0,0,0,1,1,0,0,0],
    [0,0,1,1,0,1,0,0],
    [0,1,1,1,1,0,1,0],
    [0,1,1,1,1,1,1,0],
])

Z = np.array([
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,1,1,1,1,0,0,0],
    [0,0,0,0,1,0,0,0],
    [0,0,0,1,0,0,0,0],
    [0,0,1,0,0,0,0,0],
    [0,1,0,0,0,0,0,0],
    [0,1,1,1,1,0,0,0],
])

zzz = np.array([
    [0,0,0,0,1,1,1,0],
    [0,0,0,0,0,0,1,0],
    [0,0,0,0,0,1,0,0],
    [0,0,0,0,1,0,0,0],
    [0,0,1,0,1,1,1,0],
    [1,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
])

M = np.array([
    [0,0,0,0,0,0,0,0],
    [0,1,1,0,1,1,1,0],
    [0,1,0,1,0,1,1,0],
    [0,1,0,1,0,1,1,0],
])

arrow = np.array([
    [0,0,0,0,0,0,0,0],
    [0,0,0,1,0,0,0,0],
    [0,0,0,1,1,0,0,0],
    [0,1,1,1,1,1,0,0],
    [0,1,1,1,1,1,1,0],
    [0,1,1,1,1,1,0,0],
    [0,0,0,1,1,0,0,0],
    [0,0,0,1,0,0,0,0],
])

dead1 = np.array([
    [0,1,0,0,0,1,0,0],
    [1,0,0,0,0,1,0,0],
    [0,1,1,1,0,1,0,0],
    [0,0,1,0,1,0,0,0],
    [0,1,1,0,0,0,0,0],
    [1,0,1,0,0,0,0,0],
    [1,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
])

dead2 = np.array([
    [0,0,0,0,0,0,0,0],
    [0,1,0,0,0,1,0,0],
    [0,0,0,1,0,0,0,0],
    [0,0,1,0,1,0,0,0],
    [0,0,0,1,0,0,0,0],
    [0,1,0,0,0,1,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
])

yr = np.array([
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,1,0,1,0,1,0,1],
    [0,1,0,1,0,1,1,0],
    [0,1,0,1,0,1,0,0],
    [0,0,1,1,0,1,0,0],
    [0,0,0,1,0,1,0,0],
    [0,1,1,0,0,0,0,0],
])

egg1 = np.array([
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0],
    [0,0,0,0,0,1,1,1,1,1,1,0,0,0,0,0],
    [0,0,0,0,1,0,1,1,1,1,0,1,0,0,0,0],
    [0,0,0,1,0,0,1,1,1,1,0,0,1,0,0,0],
    [0,0,1,1,0,1,1,1,1,1,1,1,1,1,0,0],
    [0,0,1,1,1,1,1,0,0,1,1,1,1,1,0,0],
    [0,0,1,0,0,1,1,0,0,1,1,1,1,1,0,0],
    [0,0,0,1,0,0,1,1,1,1,0,0,1,0,0,0],
    [0,0,0,0,1,1,1,1,1,1,0,1,0,0,0,0],
    [0,0,0,1,1,1,1,1,1,1,1,1,1,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
])

egg2 = np.array([
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0],
    [0,0,0,0,0,1,0,1,1,1,1,0,0,0,0,0],
    [0,0,0,0,1,0,0,1,1,0,1,1,0,0,0,0],
    [0,0,0,0,1,0,1,1,1,0,0,1,0,0,0,0],
    [0,0,0,1,1,1,1,1,1,1,1,1,1,0,0,0],
    [0,0,0,1,1,1,1,0,0,1,1,1,1,0,0,0],
    [0,0,0,1,1,1,1,0,0,1,0,0,1,0,0,0],
    [0,0,0,1,0,0,1,1,1,1,0,1,1,0,0,0],
    [0,0,0,0,1,0,0,1,1,1,1,1,0,0,0,0],
    [0,0,0,0,0,1,1,1,0,0,1,0,0,0,0,0],
    [0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
])

egg3 = np.array([
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,1,1,1,1,1,1,0,0,0,0,0],
    [0,0,0,0,1,1,1,0,0,1,1,1,0,0,0,0],
    [0,0,0,1,0,1,1,0,0,1,1,0,1,0,0,0],
    [0,0,0,1,1,0,0,1,1,0,0,1,1,0,0,0],
    [0,0,1,1,1,0,0,1,1,0,0,1,1,1,0,0],
    [0,0,1,0,0,1,1,0,0,1,1,0,0,1,0,0],
    [0,0,1,0,0,1,1,0,0,1,1,0,0,1,0,0],
    [0,0,1,1,1,0,0,1,1,0,0,1,1,1,0,0],
    [0,0,0,1,1,0,0,1,1,0,0,1,1,0,0,0],
    [0,0,0,0,1,1,1,0,0,1,1,1,0,0,0,0],
    [0,0,0,1,1,1,1,1,1,1,1,1,1,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
])

egg4 = np.array([
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0],
    [0,0,0,0,0,1,1,0,0,1,1,0,0,0,0,0],
    [0,0,0,0,1,1,1,0,0,1,1,1,0,0,0,0],
    [0,0,0,0,1,0,0,1,1,0,0,1,0,0,0,0],
    [0,0,0,1,1,0,0,1,1,0,0,1,1,0,0,0],
    [0,0,0,1,0,1,1,0,0,1,1,0,1,0,0,0],
    [0,0,1,0,0,1,1,0,0,1,1,0,0,1,0,0],
    [0,0,1,1,1,0,0,1,1,0,0,1,1,1,0,0],
    [0,0,1,1,1,0,0,1,1,0,0,1,1,1,0,0],
    [0,0,0,1,0,1,1,0,0,1,1,0,1,0,0,0],
    [0,0,0,0,1,1,1,0,0,1,1,1,0,0,0,0],
    [0,0,0,0,0,1,0,1,1,0,1,0,0,0,0,0],
    [0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
])

### Checks

def is_sick(tama):
    return np.all(top_right(tama) == skull)

def is_dirty(tama, x="top"):
    if x == "top":
        to_check = top_right(tama)
    elif x == "bottom":
        to_check = bottom_right(tama)
    else:
        raise ValueError("x must be 'top' or 'bottom'")
    return np.all(to_check == poop1) or np.all(to_check == poop2)

def is_asleep(tama, x="on"):
    if x == "on":
        to_check = top_right(tama)
        return np.all(to_check == Z) or np.all(to_check == zzz)
    elif x == "off":
        to_check = tama.Matrix()[0:8, 16:24]
        return np.all(to_check == (1 - Z)) or np.all(to_check == (1 - zzz))
    else:
        raise ValueError("x must be 'on' or 'off'")

def is_dark(tama):
    return np.all(tama.Matrix() == 1)

def is_clock(tama):
    return np.all(tama.Matrix()[12:16, 2:10] == M)

def is_burger(tama):
    return np.all(tama.Matrix()[0:8, 0:8] == arrow)

def is_dead(tama):
    to_check = bottom_right(tama)
    return (
        np.all(to_check == dead1) or
        np.all(to_check == dead2) or
        np.all(to_check == yr)
    )

def nb_hearts(tama):
    to_check = tama.Matrix()[8:16, :]
    h1 = np.all(to_check[:, 0:8] == heart)
    h2 = np.all(to_check[:, 8:16] == heart)
    h3 = np.all(to_check[:, 16:24] == heart)
    h4 = np.all(to_check[:, 24:32] == heart)
    return 4 - h1 - h2 - h3 - h4

def is_egg(tama, egg1 = egg1, egg2 = egg2):
    pic1 = tama.Matrix()[0:16,8:24]
    time.sleep(.25)
    pic2 = tama.Matrix()[0:16,8:24]
    return (

        # p1
        np.all(pic1 == egg1) or
        np.all(pic1 == egg2) or
        np.all(pic2 == egg1) or
        np.all(pic2 == egg2) or
        
        # p2
        np.all(pic1 == egg3) or
        np.all(pic1 == egg4) or
        np.all(pic2 == egg3) or
        np.all(pic2 == egg4)
    )

### Actions

empty_todo = {
    "actions": [],
    "wait": .25
}

out = ["C","C",2]

def set_clock():
    todo = {
        "actions": ["B",1.5],
        "wait": 3
    }

    now = time.localtime()
    hr = int(time.strftime("%H", now))
    mn = int(time.strftime("%M", now))
    print(f"initialization at {hr}:{mn}")

    if hr > 0:
        for _ in range(hr):
            todo["actions"].append("A")

    if mn > 0:
        for _ in range(mn):
            todo["actions"].append("B")
    
    todo["actions"].extend(["C", "B", 310])
    
    return todo

def check_food_arrow():
    todo = empty_todo.copy()
    todo["actions"] = ["A", "B", 1]
    return todo

def feed(x="top", times=1):
    todo = empty_todo.copy()
    if x == "bottom":
        todo["actions"] = ["A"]
    for _ in range(times):
        todo["actions"].extend(["B", 6])
    todo["actions"].extend(out)
    return todo

def light():
    todo = empty_todo.copy()
    todo["actions"] = ["A"] * 2 + ["B", "A", "B"] + out
    return todo

def play_game(times=1):
    todo = empty_todo.copy()
    todo["actions"] = ["A"] * 3 + ["B"]

    for _ in range(times):
        playlist = random.choices(["A", "B"], k=5)
        interleaved = []
        for p in playlist:
            interleaved.append(p)
            interleaved.append(8)
        todo["actions"].extend(
            [5] +           # intro
            interleaved +   # chaque match + résultat
            [8]             # score final + résultat
        )
    todo["actions"].extend(out)
    return todo

def heal():
    todo = empty_todo.copy()
    todo["actions"] = ["A"] * 4 + ["B", 6] * 2 + out # 2 doses
    return todo

def clean():
    todo = empty_todo.copy()
    todo["actions"] = ["A"] * 5 + ["B", 8] + out
    return todo

def check_status(step=1):
    todo = empty_todo.copy()
    if step == 1:
        todo["actions"] = ["A"] * 6 + [
            "B", 2, # age & weight
            "B", 2, # discipline
            "B", 2  # hunger
        ]
    elif step == 2:
        todo["actions"] = ["B", 2] # happiness
    elif step == 3:
        todo["actions"] = out.copy()
    return todo

def scold():
    todo = empty_todo.copy()
    todo["actions"] = ["A"] * 7 + ["B", 6] + out
    return todo

def unclock():
    todo = empty_todo.copy()
    todo["actions"] = ["B", 5]
    return todo

### Initial state

state0 = {
    "t0": time.time(),
    "todo": empty_todo,
    "dead": False,
    "doing": "",
    "stats": {
        "hunger": 4, # nb of full hearts
        "happiness": 4
    },
    "scold": False,
    "egg": True,
    "next_check": 0
}

### Care step & global algorithmics

def carestep(tama, state, param):

    t1 = time.time()
    elapsed = t1 - state["t0"]
    state["t0"] = t1

    ### if it's an egg, set the clock
    if state["egg"]:
        if is_egg(tama):
            state["todo"] = set_clock()
        state["egg"] = False

    ### if dead, that's over
    if is_dead(tama):
        state["dead"] = True
        state["todo"]["wait"] = float('inf')

    ### stop the need to scold if it doesn't cry anymore
    if not tama.icons()[7]:
        state["scold"] = False
    
    ### otherwise, plan an action
    if is_asleep(tama, "off"):
        state["stats"] = {
            "hunger": 4,
            "happiness": 4
        }
    elif state["todo"]["wait"] <= 0 and len(state["todo"]["actions"]) == 0:

        # end what has been started
        if state["doing"] != "":
            if state["doing"] == "try_to_clean":
                if is_dirty(tama, "top"):
                    # still dirty => asleep, turn the light off
                    state["todo"] = light()
                    state["doing"] = ""

            elif state["doing"] == "check_arrow":
                # now that the arrow is checked, feed
                side = "top" if is_burger(tama) else "bottom"
                state["todo"] = feed(side, times=4 - state["stats"]["hunger"])
                state["stats"]["hunger"] = 4
                state["doing"] = ""

            elif state["doing"] == "check_status_1":
                # check hunger
                state["stats"]["hunger"] = nb_hearts(tama)
                state["todo"] = check_status(step = 2)
                state["doing"] = "check_status_2"

            elif state["doing"] == "check_status_2":
                # check happiness
                state["stats"]["happiness"] = nb_hearts(tama)
                state["todo"] = check_status(step = 3)
                state["doing"] = ""

                if (
                    tama.icons()[7] and
                    not is_asleep(tama, "on") and
                    state["stats"]["hunger"] > 0 and
                    state["stats"]["happiness"] > 0
                ):
                    state["scold"] = True

        # check bad screens (clock, light off when not asleep)
        elif is_clock(tama):
            state["todo"] = unclock()

        elif is_dark(tama):
            state["todo"] = light()

        # cares
        elif is_asleep(tama,"on"):
            state["todo"] = light()

        elif is_dirty(tama, "top"):
            # double poop: try to clean - or is it asleep ?
            state["todo"] = clean()
            state["doing"] = "try_to_clean"

        elif is_dirty(tama, "bottom"):
            state["todo"] = clean()

        elif is_sick(tama):
            # heal after double poop that may hide it
            state["todo"] = heal()

        elif param["disc"] and state["scold"]:
            state["todo"] = scold()
            state["scold"] = True

        elif state["stats"]["hunger"] < 4 and not state["scold"]:
            state["todo"] = check_food_arrow()
            state["doing"] = "check_arrow"

        elif state["stats"]["happiness"] < 4 and not state["scold"]:
            state["todo"] = play_game(times = min(2, 4 - state["stats"]["happiness"]))
            state["stats"]["happiness"] = 4
            state["next_check"] = 0

            # if it's time and it's not sleeping,
            # or if it's crying with no apparent reason
            # reasons: light on when sleeping, hungry, unhappy, to scold
            # hungry and unhappy must be checked, if checked and !=0: "to scold"
        elif (
            state["t0"] > state["next_check"] or
            (
                tama.icons()[7] and
                not is_asleep(tama, "on")
            )
        ):
            state["next_check"] = state["t0"] + param["check_every"]
            state["todo"] = check_status(step=1)
            state["doing"] = "check_status_1"
            state["scold"] = False  # we will check that

    ### do what has been planned
    if state["todo"]["wait"] > 0:
        state["todo"]["wait"] = state["todo"]["wait"] - elapsed
    else:
        if len(state["todo"]["actions"]) > 0:

            act = state["todo"]["actions"][0]

            if act in ["A","B","C"]:
                tama.click(act, .1)
                state["todo"]["wait"] =  .4
            else:
                state["todo"]["wait"] = act

            state["todo"]["actions"].pop(0)
        
    return state

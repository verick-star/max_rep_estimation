from bakery import assert_equal
from drafter import *
from dataclasses import dataclass

hide_debug_information()
set_website_title("1 Rep Max")
set_site_information(author="Van Erickson",
                     description="This website will predict a person 1 Rep Max for either bench press, squat, or deadlift based off of previous amounts of reps and weight.",
                     sources="The drafter documentation and Copilot LLM",
                     planning=["https://docs.google.com/document/d/1wJN3k1rGrB8Ny9avM_Wb5uqi4e7gfr0kTqzOgyP3qj4/edit?tab=t.0", "https://docs.google.com/document/d/1H47pgEkQBFCShDhxItnpazxp62HK1iWOSrWROEPZ5Zg/edit?tab=t.0", "Copilot LLM"],
                     links="https://verick-star.github.io/max_rep_estimation/"

    
)
set_website_framed(False)

from bakery import assert_equal
from dataclasses import dataclass
from drafter import *

@dataclass
class Lift:
    """Stores information about a single lift attempt."""
    exercise: str
    weight: float
    reps: int
    max: float

@dataclass
class State:
    """Stores user information and lift history."""
    name: str
    bodyweight: float
    history: list[Lift]
    total_calculations: int

def calculate_1rm(weight: float, reps: int) -> float:
    """Calculates an estimated one rep max using the Epley formula."""
    return round(weight * (1 + reps / 30), 2)

@route
def formulas(state: State):
    """Displays information about the 1RM formula used in the application."""
    return Page(state, [
        "1RM Formula Information:",
        "",
        "This application uses the Epley Formula to estimate your One Rep Max.",
        "",
        "1RM = Weight × (1 + Reps / 30)",
        "",
        "Example:",
        "If you lift 225 lbs for 5 reps:",
        "1RM = 225 × (1 + 5/30)",
        "Estimated 1RM = 262.5 lbs",
        "",
        Button("Home", index)
    ])

@route
def index(state: State):
    """Displays the home page of the application."""
    return Page(state, [
        "1 Rep Max Calculator",
        Button("Go to Calculator", calculator),
        Button("View History", history),
        Button("Formula Info", formulas),
        Button("Best Lift", comparison),
        Button("Leaderboard", leaderboard),
        Button("About", about)
    ])

@route
def calculator(state: State):
    """Allows the user to enter personal and lift information."""
    return Page(state, [
        "Calculate Your 1RM:",
        "",
        "Enter your name:",
        TextBox("name"),
        "",
        "Enter your body weight (lbs):",
        TextBox("bodyweight"),
        "",
        "Select a lift:",
        SelectBox(
            "exercise",
            ["Bench Press", "Squat", "Deadlift"]
        ),
        "",
        "Weight lifted (lbs):",
        TextBox("weight"),
        "",
        "Number of reps:",
        TextBox("reps"),
        "",
        Button("Calculate 1RM", results)
    ])

@route
def results(state: State,
            name: str,
            bodyweight: float,
            exercise: str,
            weight: float,
            reps: int):
    """Calculates, stores, and displays the user's estimated one rep max."""
    one_rm = calculate_1rm(weight, reps)

    state.name = name
    state.bodyweight = bodyweight

    new_lift = Lift(
        exercise,
        weight,
        reps,
        one_rm
    )

    state.history.append(new_lift)
    state.total_calculations += 1

    return Page(state, [
        "Congrats " +
        name +
        "! Your estimated 1 rep max for " +
        exercise +
        " is " +
        str(one_rm) +
        " lbs.",
        Button("Calculator", calculator),
        Button("History", history),
        Button("Home", index)
    ])

@route
def history(state: State):
    """Displays all previously recorded lifts."""
    content = ["Lift History:"]

    if len(state.history) == 0:
        content.append("No lifts recorded.")
    else:
        for lift in state.history:
            content.append(
                lift.exercise +
                ": " +
                str(lift.weight) +
                " lbs x " +
                str(lift.reps) +
                " reps (1RM = " +
                str(lift.max) +
                ")"
            )

    
    
    return Page(state, content + [Button("Home", index)])

@route
def comparison(state: State):
    """Displays the lift with the highest estimated one rep max."""
    if len(state.history) == 0:
        return Page(state, [
            "No lifts recorded yet.",
            Button("Home", index)
        ])

    best = state.history[0]

    for lift in state.history:
        if lift.max > best.max:
            best = lift

    return Page(state, [
        "Best Lift:",
        best.exercise,
        "Estimated 1RM: " + str(best.max),
        Button("Home", index)
    ])

@route
def leaderboard(state: State):
    """Displays all lifts ranked from highest to lowest estimated one rep max."""
    content = ["Leaderboard:"]

    if len(state.history) == 0:
        content.append("No lifts recorded.")
    else:
        """
        the sorted() just sorts the list of lifts with the key being lift.max
        so the new sorted list goes from highest max to lowest max
        """
        sorted_lifts = sorted(
            state.history,
            key=lambda lift: lift.max,
            reverse=True
        )

        position = 1

        for lift in sorted_lifts:
            content.append(
                str(position) +
                ". " +
                lift.exercise +
                " (" +
                str(lift.max) +
                ")"
            )
            position += 1

    

    return Page(state, content + [Button("Home", index)])

@route
def about(state: State):
    """Displays information about the purpose of the application."""
    return Page(state, [
        "About:",
        "This application estimates a user's one rep max for Bench Press, Squat, and Deadlift.",
        Button("Home", index)
    ])





start_server(
    State(
        "",
        0.0,
        [],
        0
    )
)

from dataclasses import dataclass, field
from drafter import *

set_website_title("Game Picker")
set_site_information(
    author="James Kocher",
    description="A website that recommends video games based on genre, platform, and multiplayer preferences.",
    sources="Created using Python and the Drafter library.",
    planning=[
        "planning.docx",
        "design.docx"
    ],
    links=[
        "https://docs.google.com/document/d/1iyPYtaattIEXf6_q2tckGRXXW6qlqopNzrsOyaP_uk0/edit",
        "https://docs.google.com/document/d/13gpaOdGKijB_k4sh4vGotj1ypl9es86kRcm19k4x9VM/edit"
    ]
)


hide_debug_information()
set_website_framed(False)

@dataclass
class Game:
    name: str
    genre: str
    platform: str
    multiplayer: bool


@dataclass
class State:
    name: str = ""
    genre: str = "Any"
    platform: str = "Any"
    multiplayer: str = "Any"
    games: list[Game] = field(default_factory=list)
    favorites: list[str] = field(default_factory=list)


def create_games():
    games = [
        Game("Minecraft", "Adventure", "PC", True),
        Game("Fortnite", "Action", "PlayStation", True),
        Game("Forza Horizon 5", "Racing", "Xbox", True),
        Game("The Sims 4", "Simulation", "PC", False),
        Game("Mario Kart 8", "Racing", "Nintendo Switch", True),
        Game("God of War", "Action", "PlayStation", False),
        Game("Stardew Valley", "Simulation", "PC", False),
        Game("Halo Infinite", "Action", "Xbox", True),
        Game("Zelda: Breath of the Wild", "Adventure",
             "Nintendo Switch", False),
        Game("Rocket League", "Racing", "PC", True)
    ]

    return games


def find_games(state: State):
    matching_games = []

    for game in state.games:

        if state.genre != "Any":
            if game.genre != state.genre:
                continue

        if state.platform != "Any":
            if game.platform != state.platform:
                continue

        if state.multiplayer == "Yes":
            if game.multiplayer == False:
                continue

        if state.multiplayer == "No":
            if game.multiplayer == True:
                continue

        matching_games.append(game)

    return matching_games


# HOME PAGE

@route

@route
def index(state: State) -> Page:

    if state.name == "":
        greeting = "Welcome!"
    else:
        greeting = "Welcome, " + state.name + "!"

    return Page(state, [
        Header("Video Game Picker"),
        Paragraph("Welcome to my video game recommendation website!"),
        Paragraph("This website will help you find games based on your preferences."),

        Header(greeting, 2),

        Paragraph("Enter your name:"),
        TextBox("name_input", state.name),
        Button("Save Name", "save_name"),

        HorizontalRule(),

        Link("Get Started", "picker"),
        LineBreak(),
        Link("View All Games", "all_games"),
        LineBreak(),
        Link("My Favorites", "favorites")
    ])



# GAME PICKER PAGE

@route
def picker(state: State) -> Page:
    return Page(state, [
        Header("Game Picker"),
        Paragraph("Choose what type of game you want to play."),

        Paragraph("Choose a genre:"),
        SelectBox("genre", [
            "Any", "Action", "Adventure",
            "Racing", "Simulation"
        ]),

        Paragraph("Choose your platform:"),
        SelectBox("platform", [
            "Any", "PC", "Xbox",
            "PlayStation", "Nintendo Switch"
        ]),

        Paragraph("Do you want multiplayer?"),
        SelectBox("multiplayer", [
            "Any", "Yes", "No"
        ]),

        Button("Find Games", "save_preferences"),
        Link("Back to Home", "back_home")
    ])


# SAVE PREFERENCES

@route
def save_preferences(state: State,
                     genre: str,
                     platform: str,
                     multiplayer: str) -> Page:

    state.genre = genre
    state.platform = platform
    state.multiplayer = multiplayer

    return results(state)


# RESULTS PAGE

@route
def results(state: State) -> Page:

    matching_games = find_games(state)

    content = [
        Header("Recommended Games"),
        Paragraph("Here are games based on your choices.")
    ]

    if len(matching_games) == 0:
        content.append(
            Paragraph("No games matched your preferences.")
        )
    else:
        for game in matching_games:
            content.append(Header(game.name, 3))
            content.append(
                Paragraph("Genre: " + game.genre)
            )
            content.append(
                Paragraph("Platform: " + game.platform)
            )

    content.append(Link("Try Again", "picker"))
    content.append(Link("Back to Home", "index"))

    return Page(state, content)


# ALL GAMES PAGE

@route
def all_games(state: State) -> Page:

    content = [
        Header("All Video Games"),
        Paragraph("Here are all the games on our website.")
    ]

    for game in state.games:
        content.append(Header(game.name, 3))

        content.append(
            Button(
                "View Details",
                "game_details",
                [Argument("game_name", game.name)]
            )
        )

        content.append(
            Paragraph("Genre: " + game.genre)
        )

        content.append(
            Paragraph("Platform: " + game.platform)
        )

        if game.multiplayer:
            content.append(
                Paragraph("Multiplayer: Yes")
            )
        else:
            content.append(
                Paragraph("Multiplayer: No")
            )

    content.append(Link("Back to Home", "index"))

    return Page(state, content)


# GAME DETAILS PAGE

@route
def game_details(state: State, game_name: str) -> Page:

    for game in state.games:
        if game.name == game_name:

            if game.multiplayer:
                multiplayer_text = "Yes"
            else:
                multiplayer_text = "No"

            return Page(state, [
                Header(game.name),
                Paragraph("Genre: " + game.genre),
                Paragraph("Platform: " + game.platform),
                Paragraph("Multiplayer: " + multiplayer_text),

                Button(
                    "Add to Favorites",
                    "add_favorite",
                    [Argument("game_name", game.name)]
                ),

                Link("Back to All Games", "all_games"),
                Link("Back to Home", "index")
            ])

    return Page(state, [
        Header("Game Not Found"),
        Paragraph("Sorry, that game was not found."),
        Link("Back to All Games", "all_games")
    ])


# BACK TO HOME

@route
def back_home(state: State, genre: str,
              platform: str, multiplayer: str) -> Page:

    return index(state)


# ADD FAVORITE

@route
def add_favorite(state: State, game_name: str) -> Page:

    if game_name not in state.favorites:
        state.favorites.append(game_name)

    return game_details(state, game_name)


# REMOVE FAVORITE

@route
def remove_favorite(state: State, game_name: str) -> Page:

    if game_name in state.favorites:
        state.favorites.remove(game_name)

    return game_details(state, game_name)


# FAVORITES PAGE

@route
def favorites(state: State) -> Page:

    content = [
        Header("My Favorite Games")
    ]

    if len(state.favorites) == 0:
        content.append(
            Paragraph("You have no favorite games yet.")
        )

    for game in state.games:
        if game.name in state.favorites:
            content.append(Header(game.name, 3))
            content.append(
                Button(
                    "Remove Favorite",
                    "remove_favorite",
                    [Argument("game_name", game.name)]
                )
            )

    content.append(Link("Back to All Games", "all_games"))
    content.append(Link("Back to Home", "index"))

    return Page(state, content)

@route
def save_name(state: State, name_input: str) -> Page:

    state.name = name_input

    return index(state)

# START WEBSITE

start_server(State(games=create_games()))


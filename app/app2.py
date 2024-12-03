from shiny import App, ui
import palmerpenguins

# Load the Palmer Penguins dataset into a DataFrame
df = palmerpenguins.load_penguins()

app_ui = ui.page_fillable(
    ui.layout_sidebar(
        ui.sidebar(
            # Sidebar layout for input controls
            ui.input_slider("mass", "Mass", 2000, 6000, 6000),
            ui.hr(),  # Horizontal rule for separating sections
            ui.input_checkbox_group(
                "species",
                "Species",
                ["Adelie", "Gentoo", "Chinstrap"],  # Available species
                selected=["Adelie", "Gentoo", "Chinstrap"],  # Default selection
            ),
            title="Filter controls",  # Title for the sidebar
            bg="#f8f8f8",  # Background color for the sidebar
        ),
        ui.card(
            ui.card_header("Penguin Dashboard"),
            ui.navset_tab(
                ui.nav_panel("A", "Panel A content"),
                ui.nav_panel("B", "Panel B content"),
                ui.nav_panel("C", "Panel C content"),
                ui.nav_panel("D", "Panel D content"),
                ui.nav_panel("E", "Panel E content"),
                ui.nav_panel("F", "Panel F content"),
                ui.nav_menu(
                    "Links",
                    ui.nav_control(
                        ui.a("Shiny", href="https://shiny.posit.co", target="_blank")
                    ),
                    ui.nav_control(
                        ui.a(
                            "GitHub Source",
                            href="https://github.com/denisecase/cintel-07-tdash",
                            target="_blank",
                        )
                    ),
                    ui.nav_control(
                        ui.a(
                            "GitHub App",
                            href="https://denisecase.github.io/cintel-07-tdash/",
                            target="_blank",
                        )
                    ),
                    ui.nav_control(
                        ui.a(
                            "GitHub Issues",
                            href="https://github.com/denisecase/cintel-07-tdash/issues",
                            target="_blank",
                        )
                    ),
                    ui.nav_control(
                        ui.a(
                            "PyShiny",
                            href="https://shiny.posit.co/py/",
                            target="_blank",
                        )
                    ),
                    ui.nav_control(
                        ui.a(
                            "Template: Basic Dashboard",
                            href="https://shiny.posit.co/py/templates/dashboard/",
                            target="_blank",
                        )
                    ),
                    ui.nav_control(
                        ui.a(
                            "See also",
                            href="https://github.com/denisecase/pyshiny-penguins-dashboard-express",
                            target="_blank",
                        )
                    ),
                ),
                id="tab",
            ),
        ),
    )
)


def server(input, output, session):
    pass


app = App(app_ui, server)

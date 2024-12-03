from shiny import App, ui

app_ui = ui.page_fillable(
    ui.layout_sidebar(
        ui.sidebar("Sidebar", bg="#f8f8f8"),
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

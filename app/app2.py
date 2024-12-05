from shiny import App, ui, render
import palmerpenguins
import seaborn as sns
import matplotlib.pyplot as plt

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
                ui.nav_panel(
                    "B",
                    ui.layout_columns(
                        # Correct argument order: Positional arguments before keyword arguments
                        ui.card(
                            ui.card_header("Bill length and depth"),
                            ui.output_plot("length_depth_plot"),  # Placeholder for the plot
                            full_screen=True,  # Keyword argument comes last
                        )
                    ),
                ),
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
                            target="_blank"
                        )
                    ),
                    ui.nav_control(
                        ui.a(
                            "Template: Basic Dashboard",
                            href="https://shiny.posit.co/py/templates/dashboard/",
                            target="_blank"
                        )
                    ),
                    ui.nav_control(
                        ui.a(
                            "See also",
                            href="https://github.com/denisecase/pyshiny-penguins-dashboard-express",
                            target="_blank"
                        )
                    ),
                ),
                id="tab",  # This is the keyword argument
            ),
        ),
    )
)


def server(input, output, session):
    @output
    @render.plot
    def length_depth_plot():
        # Filter the DataFrame based on selected species and mass
        selected_species = input.species()
        max_mass = input.mass()
        filtered_df = df[(df['species'].isin(selected_species)) & (df['body_mass_g'] <= max_mass)]

        # Generate scatter plot
        plt.figure(figsize=(8, 6))
        sns.scatterplot(
            data=filtered_df,
            x="bill_length_mm",
            y="bill_depth_mm",
            hue="species",
            palette="muted",
        )
        plt.title("Bill Length vs Depth")
        return plt.gcf()  # Return the current figure


app = App(app_ui, server)

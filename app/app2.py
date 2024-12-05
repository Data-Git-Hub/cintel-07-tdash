from shiny import App, ui, render, reactive
import palmerpenguins
import seaborn as sns  # Import Seaborn for scatter plot generation
import matplotlib.pyplot as plt  # Required for plot rendering

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
                ui.nav_panel(
                    "A",
                    ui.layout_columns(
                        ui.card("Card 1"),
                        ui.card("Card 2"),
                        ui.card("Card 3"),
                        col_widths=(4, 4, 4),  # Equally distributed column widths
                    ),
                ),
                ui.nav_panel(
                    "B",
                    ui.layout_columns(
                        # Correct argument order: Positional arguments before keyword arguments
                        ui.card(
                            ui.card_header("Bill length and depth"),
                            ui.output_plot(
                                "length_depth_plot"
                            ),  # Placeholder for the plot
                            full_screen=True,  # Keyword argument comes last
                        )
                    ),
                ),
                ui.nav_panel("C", "Panel C content"),
                ui.nav_panel("D", "Panel D content"),
                ui.nav_panel("E", "Panel E content"),
                ui.nav_panel(
                    "F",
                    ui.card(
                        ui.card_header("Penguin Data"),
                        ui.output_data_frame(
                            "summary_statistics"
                        ),  # Placeholder for data table
                        full_screen=True,
                    ),
                ),
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
                id="tab",  # This is the keyword argument
            ),
        ),
    )
)


def server(input, output, session):
    # Reactive calculation to filter the dataset based on user input
    @reactive.Calc
    def filtered_df():
        # Filter data by selected species
        filt_df = df[df["species"].isin(input.species())]
        # Further filter data by body mass
        filt_df = filt_df.loc[filt_df["body_mass_g"] < input.mass()]
        return filt_df

    # Render function to generate the scatter plot on Tab "B"
    @output
    @render.plot
    def length_depth_plot():
        # Generate scatter plot
        plt.figure(figsize=(8, 6))
        sns.scatterplot(
            data=filtered_df(),
            x="bill_length_mm",
            y="bill_depth_mm",
            hue="species",
            palette="muted",
        )
        plt.title("Bill Length vs Depth")
        return plt.gcf()  # Return the current figure

    # Render function to generate the data table on Tab "F"
    @output
    @render.data_frame
    def summary_statistics():
        cols = [
            "species",
            "island",
            "bill_length_mm",
            "bill_depth_mm",
            "body_mass_g",
        ]
        # Return the filtered data with specified columns
        return render.DataGrid(filtered_df()[cols], filters=True)


app = App(app_ui, server)

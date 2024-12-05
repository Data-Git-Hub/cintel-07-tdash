from shiny import App, ui, render, reactive
import palmerpenguins
import matplotlib.pyplot as plt
import io
from base64 import b64encode
import seaborn as sns

# Load the Palmer Penguins dataset into a DataFrame
df = palmerpenguins.load_penguins()

# Define the UI layout
app_ui = ui.page_fillable(
    ui.layout_sidebar(
        ui.sidebar(
            ui.input_slider("mass", "Mass", 2000, 6000, 6000),
            ui.hr(),
            ui.input_checkbox_group(
                "species",
                "Species",
                ["Adelie", "Gentoo", "Chinstrap"],
                selected=["Adelie", "Gentoo", "Chinstrap"],
            ),
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
                        col_widths=(4, 4, 4),
                    ),
                ),
                ui.nav_panel(
                    "B",
                    ui.layout_columns(
                        ui.card(
                            ui.card_header("Bill length and depth"),
                            ui.output_plot("length_depth_plot"),
                            full_screen=True,
                        )
                    ),
                ),
                ui.nav_panel(
                    "C",
                    ui.card(
                        ui.card_header("Histogram"),
                        ui.input_selectize(
                            "var",
                            "Select variable",
                            choices=["bill_length_mm", "bill_depth_mm", "body_mass_g"],
                        ),
                        ui.output_ui("hist_plot"),
                    ),
                ),
                ui.nav_panel("D", "Panel D content"),
                ui.nav_panel("E", "Panel E content"),
                ui.nav_panel(
                    "F",
                    ui.card(
                        ui.card_header("Penguin Data"),
                        ui.output_data_frame("summary_statistics"),
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
                id="tab",
            ),
        ),
    )
)

# Server logic
def server(input, output, session):
    # Reactive filtered DataFrame
    @reactive.Calc
    def filtered_df():
        filt_df = df[df["species"].isin(input.species())]
        filt_df = filt_df.loc[filt_df["body_mass_g"] < input.mass()]
        return filt_df

    # Render scatter plot for Tab "B"
    @output
    @render.plot
    def length_depth_plot():
        plt.figure(figsize=(8, 6))
        sns.scatterplot(
            data=filtered_df(),
            x="bill_length_mm",
            y="bill_depth_mm",
            hue="species",
            palette="muted",
        )
        plt.title("Bill Length vs Depth")
        return plt.gcf()

    # Render histogram for Tab "C"
    @output
    @render.ui
    def hist_plot():
        data = filtered_df()
        var = input.var()

        # Create a Matplotlib figure
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.hist(data[var].dropna(), bins=30, color="skyblue", edgecolor="black")
        ax.set_title(f"Histogram of {var}")
        ax.set_xlabel(var)
        ax.set_ylabel("Frequency")

        # Save the figure to a BytesIO stream
        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        buf.seek(0)

        # Encode the image in base64
        img_b64 = b64encode(buf.read()).decode("utf-8")
        buf.close()
        plt.close(fig)

        # Return the image as an HTML img tag
        return ui.HTML(f'<img src="data:image/png;base64,{img_b64}" alt="Histogram">')

    # Render data table for Tab "F"
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
        return filtered_df()[cols]

# Create and run the app
app = App(app_ui, server)

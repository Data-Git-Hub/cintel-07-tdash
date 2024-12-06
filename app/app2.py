from shiny import App, ui, render, reactive
import pandas as pd  # Import pandas for DataFrame operations
import palmerpenguins
import matplotlib.pyplot as plt
import io
from base64 import b64encode
import seaborn as sns
import plotly.express as px

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
                        ui.card(
                            ui.card_header("Card 1: Number of Penguins"),
                            ui.output_text(
                                "penguin_count"
                            ),  # Output text for number of penguins
                        ),
                        ui.card(
                            ui.card_header("Card 2: Average Bill Length"),
                            ui.output_text(
                                "bill_length"
                            ),  # Output text for average bill length
                        ),
                        ui.card(
                            ui.card_header("Card 3: Average Bill Depth"),
                            ui.output_text(
                                "bill_depth"
                            ),  # Output text for average bill depth
                        ),
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
                ui.nav_panel(
                    "D",
                    ui.card(
                        ui.card_header("Plotly Histogram"),
                        ui.input_selectize(
                            "plotly_var",
                            "Select variable",
                            choices=["bill_length_mm", "body_mass_g"],
                        ),
                        ui.output_ui("plotly_hist"),
                    ),
                ),
                ui.nav_panel("E", "Panel E content"),
                ui.nav_panel(
                    "F",
                    ui.card(
                        ui.card_header("Penguin Data with Filters"),
                        ui.output_data_frame("penguins_df"),
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

    # Render number of penguins for Tab "A" Card 1
    @output
    @render.text
    def penguin_count():
        return f"Number of penguins: {filtered_df().shape[0]}"

    # Render average bill length for Tab "A" Card 2
    @output
    @render.text
    def bill_length():
        avg_length = filtered_df()["bill_length_mm"].mean()
        if pd.isna(avg_length):  # Check if average length is NaN
            return "Average bill length: No data available"
        return f"Average bill length: {avg_length:.1f} mm"

    # Render average bill depth for Tab "A" Card 3
    @output
    @render.text
    def bill_depth():
        avg_depth = filtered_df()["bill_depth_mm"].mean()
        if pd.isna(avg_depth):  # Check if average depth is NaN
            return "Average bill depth: No data available"
        return f"Average bill depth: {avg_depth:.1f} mm"

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

    # Render Plotly histogram for Tab "D"
    @output
    @render.ui
    def plotly_hist():
        var = input.plotly_var()
        fig = px.histogram(
            filtered_df(),
            x=var,
            color="species",
            title=f"Plotly Histogram of {var}",
            barmode="group",
        )
        # Convert Plotly figure to HTML
        return ui.HTML(fig.to_html(full_html=False))

    # Render filterable data table for Tab "F"
    @output
    @render.data_frame
    def penguins_df():
        return render.DataTable(filtered_df(), filters=True)


# Create and run the app
app = App(app_ui, server)

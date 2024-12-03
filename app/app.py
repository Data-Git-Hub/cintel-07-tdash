import seaborn as sns  
from faicons import icon_svg  
from shiny import reactive  
from shiny.express import input, render, ui  
import palmerpenguins  

# Load the Palmer Penguins dataset into a DataFrame
df = palmerpenguins.load_penguins()

# Page options: Sets the title and layout of the page
ui.page_opts(title="Penguins dashboard", fillable=True)

# Sidebar layout for input controls
with ui.sidebar(title="Filter controls"):
    ui.input_slider("mass", "Mass", 2000, 6000, 6000)

    # Checkbox group input for filtering by species
    ui.input_checkbox_group(
        "species",
        "Species",
        ["Adelie", "Gentoo", "Chinstrap"],  # Available species
        selected=["Adelie", "Gentoo", "Chinstrap"],  # Default selection
    )

    # Horizontal rule for separating sections
    ui.hr()

    # Links section with external resources
    ui.h6("Links")
    ui.a(
        "GitHub Source",
        href="https://github.com/denisecase/cintel-07-tdash",
        target="_blank",
    )
    ui.a(
        "GitHub App",
        href="https://denisecase.github.io/cintel-07-tdash/",
        target="_blank",
    )
    ui.a(
        "GitHub Issues",
        href="https://github.com/denisecase/cintel-07-tdash/issues",
        target="_blank",
    )
    ui.a("PyShiny", href="https://shiny.posit.co/py/", target="_blank")
    ui.a(
        "Template: Basic Dashboard",
        href="https://shiny.posit.co/py/templates/dashboard/",
        target="_blank",
    )
    ui.a(
        "See also",
        href="https://github.com/denisecase/pyshiny-penguins-dashboard-express",
        target="_blank",
    )

# Main layout for displaying value boxes
with ui.layout_column_wrap(fill=False):
        with ui.value_box(showcase=icon_svg("earlybirds")):
        "Number of penguins"

        # Render function to calculate and display the number of penguins
        @render.text
        def count():
            return filtered_df().shape[0]

    # Value box for displaying the average bill length
    with ui.value_box(showcase=icon_svg("ruler-horizontal")):
        "Average bill length"

        # Render function to calculate and display the average bill length
        @render.text
        def bill_length():
            return f"{filtered_df()['bill_length_mm'].mean():.1f} mm"

    # Value box for displaying the average bill depth
    with ui.value_box(showcase=icon_svg("ruler-vertical")):
        "Average bill depth"

        # Render function to calculate and display the average bill depth
        @render.text
        def bill_depth():
            return f"{filtered_df()['bill_depth_mm'].mean():.1f} mm"


# Layout for charts and data table
with ui.layout_columns():
        with ui.card(full_screen=True):
        ui.card_header("Bill length and depth")

        # Render function to generate the scatter plot
        @render.plot
        def length_depth():
            return sns.scatterplot(
                data=filtered_df(),  
                x="bill_length_mm",  
                y="bill_depth_mm",  
                hue="species",  
            )

    # Card for displaying a data table with summary statistics
    with ui.card(full_screen=True):
        ui.card_header("Penguin Data")

        # Render function to generate a data table with filtered data
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


# Reactive calculation to filter the dataset based on user input
@reactive.calc
def filtered_df():
    # Filter data by selected species
    filt_df = df[df["species"].isin(input.species())]
    # Further filter data by body mass
    filt_df = filt_df.loc[filt_df["body_mass_g"] < input.mass()]
    return filt_df

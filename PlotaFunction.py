import adsk.core, adsk.fusion, adsk.cam, math
import traceback

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        design = app.activeProduct

        # Create a new sketch on the xy plane
        rootComp = design.rootComponent
        sketches = rootComp.sketches
        xyPlane = rootComp.xYConstructionPlane
        sketch = sketches.add(xyPlane)

        # Function to get a single input value from the input box
        def get_input(prompt, default_value):
            input_result, cancelled = ui.inputBox(prompt, "Input", default_value)
            if cancelled:
                raise ValueError("Input cancelled by user")
            if input_result is None or input_result.strip() == "":
                raise ValueError("No input provided")
            return input_result

        # Ask user for input function
        try:
            inputBox = get_input("Enter a function y=f(x) (e.g., sin(x), log(x)): ", "math.sin(x)")
        except ValueError as e:
            ui.messageBox(str(e))
            return

        # Ask user for the range
        try:
            x_start_str = get_input("Enter the start of the range for x (e.g., 0): ", "0")
            x_end_str = get_input("Enter the end of the range for x (e.g., 110): ", "110")
            x_step_str = get_input("Enter the step size for x (e.g., 1): ", "1")
        except ValueError as e:
            ui.messageBox(str(e))
            return
        
        try:
            # Convert range inputs to integers
            x_start = int(x_start_str)
            x_end = int(x_end_str)
            x_step = int(x_step_str)
        except ValueError as e:
            ui.messageBox(f"Error converting range inputs to integers: {e}")
            return

        # Dictionary of available math functions
        math_functions = {
            'sin': math.sin,
            'cos': math.cos,
            'tan': math.tan,
            'log': math.log,
            'exp': math.exp,
            'sqrt': math.sqrt,
            'pi': math.pi,
            'e': math.e
        }

        # Generate points
        points = adsk.core.ObjectCollection.create()
        for x in range(x_start, x_end + 1, x_step):
            x_value = x / 10.0  # Adjust step for finer granularity
            try:
                # Evaluate the function
                y = eval(inputBox, {"__builtins__": None, "math": math, "x": x_value})
                points.add(adsk.core.Point3D.create(x_value, y, 0))
            except Exception as e:
                ui.messageBox(f"Skipping point at x={x_value} due to error: {e}")
                continue

        # Check if points were created
        if points.count == 0:
            ui.messageBox("No valid points were created. Please check the function and range.")
            return

        # Create the spline
        sketch.sketchCurves.sketchFittedSplines.add(points)

        # Show success message
        ui.messageBox("Spline created successfully!")

    except Exception as e:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


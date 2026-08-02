from flask import Flask, render_template, request
import joblib

app = Flask(__name__)

model = joblib.load("model/water_model.pkl")


@app.route("/")
def home():
    return render_template("index.html")
@app.route("/predict", methods=["POST"])
def predict():

    ph = float(request.form["ph"])
    hardness = float(request.form["hardness"])
    solids = float(request.form["solids"])
    chloramines = float(request.form["chloramines"])
    sulfate = float(request.form["sulfate"])
    conductivity = float(request.form["conductivity"])
    organic_carbon = float(request.form["organic_carbon"])
    trihalomethanes = float(request.form["trihalomethanes"])
    turbidity = float(request.form["turbidity"])

    data = [[
    ph,
    hardness,
    solids,
    chloramines,
    sulfate,
    conductivity,
    organic_carbon,
    trihalomethanes,
    turbidity
]]
    # Make prediction
    prediction = model.predict(data)
    
    print("Hello")
    print(prediction)
    print("================================")
    print("PH =", ph)
    print("Hardness =", hardness)
    print("Solids =", solids)
    print("Chloramines =", chloramines)
    print("Sulfate =", sulfate)
    print("Conductivity =", conductivity)
    print("Organic Carbon =", organic_carbon)
    print("Trihalomethanes =", trihalomethanes)
    print("Turbidity =", turbidity)
    print("Prediction =", prediction)
    print("================================")

    # Display result
    if prediction[0] == 1:
        result = " Water is Safe to Drink"
        color = "safe"
    else:
        result = " Water is Not Safe to Drink"
        color = "unsafe"
        analysis = []
        
    # Water Quality Analysis
    analysis = []
    score = 0
    recommendations = []

    # pH
    if 6.5 <= ph <= 8.5:
     score += 1
     analysis.append(["pH", ph, "6.5 - 8.5", "✅ Good"])
     recommendations.append("✅ pH is within the ideal range.")
    else:
     analysis.append(["pH", ph, "6.5 - 8.5", "❌ Out of Range"])
    recommendations.append("⚠ pH should be between 6.5 and 8.5.")

    # Hardness
    if 60 <= hardness <= 200:
     score += 1
     analysis.append(["Hardness", hardness, "60 - 200", "✅ Good"])
     recommendations.append("✅ Hardness is within the recommended range.")
    else:
     analysis.append(["Hardness", hardness, "60 - 200", "❌ Out of Range"])
    recommendations.append("⚠ Hardness is outside the recommended range. Consider water softening if necessary.")

    # Solids (TDS)
    if solids <= 500:
     score += 1
     analysis.append(["Solids", solids, "<= 500", "✅ Good"])
     recommendations.append("✅ Total dissolved solids are within the recommended range.")

    else:
     analysis.append(["Solids", solids, "<= 500", "⚠ High"])
     

    # Chloramines
    if chloramines <= 4:
     score += 1
     analysis.append(["Chloramines", chloramines, "<= 4", "✅ Good"])
     recommendations.append("✅ Chloramines level is within the safe limit.")
    else:
     analysis.append(["Chloramines", chloramines, "<= 4", "⚠ High"])
     recommendations.append("⚠ Chloramines level is high. Water treatment is recommended before drinking.")

    # Sulfate
    if sulfate <= 250:
     score += 1
     analysis.append(["Sulfate", sulfate, "<= 250", "✅ Good"])
     recommendations.append("✅ Sulfate level is within the recommended limit.")
    else:
     analysis.append(["Sulfate", sulfate, "<= 250", "⚠ High"])
     recommendations.append("⚠ Sulfate level is high. Water treatment is recommended before drinking.")

    # Conductivity
    if 200 <= conductivity <= 800:
     score += 1
     analysis.append(["Conductivity", conductivity, "200 - 800", "✅ Good"])
     recommendations.append("✅ Conductivity is within the normal range.")
    else:
     analysis.append(["Conductivity", conductivity, "200 - 800", "⚠ Check"])
     recommendations.append("⚠ Conductivity is outside the normal range. Check water quality.")

    # Organic Carbon
    if organic_carbon <= 10:
     score += 1
     analysis.append(["Organic Carbon", organic_carbon, "<= 10", "✅ Good"])
     recommendations.append("✅ Organic carbon level is acceptable.")
    else:
     analysis.append(["Organic Carbon", organic_carbon, "> 10", "⚠ High"])
     recommendations.append("⚠ Organic carbon is high. Additional purification may be needed.")

    # Trihalomethanes
    if trihalomethanes <= 80:
     score += 1
     analysis.append(["Trihalomethanes", trihalomethanes, "<= 80", "✅ Good"])
     recommendations.append("✅ Trihalomethanes are within the safe limit.")
    else:
     analysis.append(["Trihalomethanes", trihalomethanes, "> 80", "⚠ High"])
    recommendations.append("⚠ Trihalomethanes exceed the safe limit. Water should be treated before drinking.")

    # Turbidity
    if turbidity <= 5:
     score += 1
     analysis.append(["Turbidity", turbidity, "<= 5", "✅ Good"])
     recommendations.append("✅ Turbidity is within the safe limit.")
    else:
     analysis.append(["Turbidity", turbidity, "> 5", "⚠ High"])
     recommendations.append("⚠ High turbidity detected. Filter the water before drinking.")
    # Calculate Water Quality Score
    water_score = round((score / 9) * 100)
    return render_template(
    "index.html",
    prediction=result,
    color=color,
    ph=ph,
    hardness=hardness,
    solids=solids,
    chloramines=chloramines,
    sulfate=sulfate,
    conductivity=conductivity,
    organic_carbon=organic_carbon,
    trihalomethanes=trihalomethanes,
    turbidity=turbidity,
    analysis=analysis,
    water_score=water_score,
    recommendations=recommendations
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
from flask.blueprints import Blueprint, request

from flask.json import jsonify




from .models import Beneficiaries

regs = Blueprint(__name__, __name__, static_url_path="/media/uploads/", 
    static_folder="media/uploads", url_prefix="joinus")
# with regs.app_context():
#     initialize_dbase(regs)


@regs.route("/registries")
def subscribers():
    registeries = Beneficiaries.query.all()
    return jsonify({
        "Full name":  registeries[0].fullname,
        "Age": registeries[0].age,
        "Phone": registeries[0].phone,
        "NIF": registeries[0].nif
    })


@regs.route("/subsribe", methods=["POST"])
def subscribe():
    data = request.args.body
    role = data["role"]
    if role in ["doctor",  "beneficiary", "caregiver"]:
        process_subscrition(role, data)
# if __name__ == "__main__":
#     app.run("0.0.0.0", port=5000, debug=True)
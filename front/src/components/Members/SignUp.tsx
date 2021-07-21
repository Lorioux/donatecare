import React from "react"
import "./SignUp.css"

interface SignUpState {
    termsOfUseLink : string,
    privacyPolicy: string,
    PrivacyProtectionPoliy: string | JSX.Element,
    ApplicationForm: JSX.Element

}

class SignUp extends React.Component<{}, SignUpState> {

    constructor(props: any){
        super(props);
        this.state = {
            termsOfUseLink : "https://#",
            privacyPolicy: "https://#",
            PrivacyProtectionPoliy: this.PrivacyProtectionPoliy(),
            ApplicationForm: this.ApplicationForm()
        }
        
        this.ApplicationForm = this.ApplicationForm.bind(this);
        this.PrivacyProtectionPoliy = this.PrivacyProtectionPoliy.bind(this);
    }

    render(){
        return(
            <div>
                {this.state.ApplicationForm}
            </div>
        )
    }

    ApplicationForm(){

        return(
            <form action="" className="signUpForm">
                {/* <label htmlFor="Name">Name</label> */}
                <input type="text" className="textField" placeholder="Name"  name="John" id="Name"/>

                {/* <label htmlFor="Surname">Surname</label> */}
                <input type="text" className="textField" name="Surname" placeholder="Doe" id="Surname"/>
                {/* <label htmlFor="DoB"></label> */}
                <input type="date" className="dateField" name="DoB" placeholder="Date of birth" id="DoB"/>

                {/* <label htmlFor="Gender">Gender</label> */}
                <input type="text" className="textField" name="Gender" placeholder="Gender" id="Gender" list="genders" />
                <datalist id="genders">
                    <option value="Male"></option>
                    <option value="Female"></option>
                    <option value="Outro"></option>
                </datalist>

                {/* <label htmlFor="Role">Role</label> */}
                <input type="text" list="roles" placeholder="Patient" />
                <datalist id="roles">
                    <option value="Patient"></option>
                    <option value="Physician"></option>
                    <option value="Care Giver"></option>
                </datalist>

                {this.PrivacyProtectionPoliy()}

                <input type="submit" value="Subscribe" name="Subscribe" />

            </form>
        )
    }

    PrivacyProtectionPoliy () {
        return (
            <div style={{
                display: "grid",
                gridTemplateColumns: "56px 1fr",
                width: "100% !important"
            }}>
                <input type="checkbox" className="check" />
                {/* <p>I understand and I bind to <a href={this.state.termsOfUseLink}> the Terms of Use </a> of CAREX Services. Also, I understand the <a href={this.state.privacyPolicy}>privacy protections policy</a> provided by CAREX.</p> */}
            </div>
        )
    }
}

export default SignUp;
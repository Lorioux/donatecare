import React, { useState } from "react";
import {render} from "react-dom"
import SignIn from "./SignIn";
import SignUp from "./SignUp";

interface MembersState {
    signInFace: JSX.Element| null,
    signUpFace: JSX.Element| null,
}

class Members extends React.Component<{}, MembersState>{
    constructor(props: any){
        super(props)
        // const [termsLink, setTermsLink] = useState();
        // const [signUp, setSignUp] = useState();
        this.state = {
            signInFace: <SignIn />,
            signUpFace: <SignUp />,
        }
    }
    
    render(){
        return[
            <div/>,
            <div style={{
                display: "flex",
                flexDirection: "row"
            }}>
                <section>
                    <span>Subscribe</span>
                    {this.state.signInFace}
                    {this.state.signUpFace}
                </section>
            </div>
        ]
    }

    Header(){
        return [
            <span>Subscribe for free</span>,
            <span className="joinusAction">SignUp</span>
        ]
    }
}

export default Members;
import React from "react";
import './SignIn.css';


class SignIn extends React.Component{

    constructor(props: any){
        super(props);
        this.state = {
            roles: [ "Doctor", "Assistant", "Patient"],
        }
    }
    
    closeDialog(e: any){
        var dlg = e.target.parentNode.parentNode;
        console.log(dlg);
        dlg.remove();
    }

    render(){
        // eslint-disable-next-line
        var dialogOpen = true;
        return(
            <div className="container"  id="signInDlg">
                <div className="titleContainer">
                    <span>
                        <h2>Hi!</h2>
                    </span>
                    <i className="closeDialog" onClick={(e)=> this.closeDialog(e)}>X</i>
                </div>
                <form className="signInForm">
                    <input
                        className="formInput"
                        type="email"
                        name="userName"
                        placeholder="username@email.xyz"
                        required
                     />

                    <input
                        className="formInput"
                        type="password"
                        name="passwd"
                        placeholder="******************"
                        required
                     />

                    <div>
                        <em>Forgot password? <a href="http://resetCredentials" target="#" rel="noopener noreferrer">Reset</a> </em>
                    </div>
                </form>
                <div className="bottonsBar">
                    <button value="Login" 
                        style={{
                            alignSelf:"flex-end"
                        }}
                    >Sign In</button>
                </div>                
            </div>
        )
    }

}

export default SignIn;
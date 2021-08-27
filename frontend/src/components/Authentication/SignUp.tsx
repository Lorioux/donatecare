import React, {useState} from "react"
import { TextField, Checkbox, Button } from "@material-ui/core";
import {Snackbar} from "@material-ui/core"
import MuiAlert, {AlertProps} from "@material-ui/lab/Alert"
import PhoneInput from "react-phone-input-2"
import "react-phone-input-2/lib/style.css"
// import axios from "axios"

import "./SignUp.css"

interface SignUpState {
    termsOfUseLink : string
    privacyPolicy: string
    PrivacyProtectionPoliy: JSX.Element | null
    signupForm: JSX.Element | null
    hasFeedback: boolean,
    feedbackSeverity: string,
    feedbackMsg: string,
    roles: Array<any>
    role : string
    genders: Array<any>
    gender: string
    phone: string
    passwdErrorMsg: string
    passwdError: boolean
    passwdmsg: string | null
}

interface SignUpProps {
    message?: string
}


const Alert = (props: AlertProps) => {
    return <MuiAlert elevation={6} variant="filled" {...props} />;
  }

const FeedbackBlock = (props: any) : JSX.Element => {
    const [open, setOpen] = useState(props.open)
    const {severity, message} = props
    const handleClose = (event?: React.SyntheticEvent, reason?: string) => {
        if (reason === 'clickaway') {
            props.closeHandler(false, null, null)
            return;
        }
    
        props.closeHandler(false, null, null)
        setOpen(false)
      };
    return (
        <Snackbar open={open} 
            autoHideDuration={6000} 
            onClose={handleClose}
            ref={props.feedref}>
            <Alert onClose={handleClose} severity={severity}>
                {message}
            </Alert>
        </Snackbar>
    )
}


class SignUp extends React.Component<SignUpProps, SignUpState> {
    private feedbackBlock : React.RefObject<JSX.Element>
    constructor(props:any){
        super(props)
        this.feedbackBlock = React.createRef()
        this.state = {
            termsOfUseLink : "https://#",
            privacyPolicy: "https://#",
            PrivacyProtectionPoliy: null,
            signupForm: <this.SignUpForm />,
            hasFeedback: false,
            feedbackSeverity: "",
            feedbackMsg: "",
            roles: [
                {label:"Doctor", value:"doctor"},
                {label:"Care Giver", value:"caregiver"},
                {label:"Patient", value:"patient"}
            ],
            role : "Doctor",
            genders: [
                {label:"Female", value:"female"},
                {label:"Male", value:"male"},
                {label:"Outro", value:"outro"}
            ],
            gender: "Female",
            phone: "",
            passwdError: false,
            passwdErrorMsg: "Password not compatible",
            passwdmsg: ""
        }
        this.SignUpForm = this.SignUpForm.bind(this)
        this.PrivacyProtectionPolicy = this.PrivacyProtectionPolicy.bind(this)
        this.onSubscriptionSubmit = this.onSubscriptionSubmit.bind(this)
        this.handleFeedback = this.handleFeedback.bind(this)
        // this.checkPassword = this.checkPassword.bind(this)
        // this.PassWordsFieldSet = this.PassWordsFieldSet.bind(this)
    }

    SignUpForm = () => {
        const {roles, role} = this.state
        const {genders, gender} = this.state
        const date = new Date()
        let month = date.getMonth()
        const amonth = month <= 8 ? `0${month + 1}` : `${month + 1}`
        return(
            <form 
                className="signUpForm" 
                method="POST"
                >
                <TextField
                    type="text"
                    select
                    className="textField"
                    defaultValue={role}
                    label="Role"
                    variant="outlined"  
                    name="myrole" 
                    id="myrole"
                    required
                    SelectProps={{
                        native:true
                    }}
                    >
                    {roles.map((role) => <option key={role.value} value={role.value}>{role.label}</option>)}

                </TextField>

                <TextField
                    type="text" 
                    className="textField" 
                    label="Name"
                    variant="outlined"  
                    name="myname" 
                    id="myname"
                    required/>

                <TextField
                    type="text" 
                    className="textField" 
                    name="surname" 
                    label="Surname"
                    variant="outlined" 
                    id="surname"
                    required/>

                
                
                <fieldset className="phone-gender-dob">
                    <div 
                        style={{
                            maxWidth:"max-content"
                        }}>
                        <PhoneInput
                            inputClass="phone"
                            inputProps={{
                                name: 'phone',
                                required: true,
                                autoFocus: true,
                            }}
                            specialLabel="Phone"
                            country={'pt'} 
                            value={this.state.phone}
                            inputStyle={{
                                height: 56,
                            }}
                            // onChange={()=> this.setState({phone})}
                            />
                        
                    </div>
                
                    <TextField 
                        type="date" 
                        className="birthday" 
                        name="dob" 
                        label="Birth date"
                        defaultValue={`${date.getFullYear()}-${amonth}-${date.getDate()}`}
                        variant="outlined"  
                        id="dob"/>

                    <TextField 
                        type="text"
                        select
                        className="gender" 
                        name="gender" 
                        label="Gender"
                        variant="outlined" 
                        id="gender"
                        defaultValue={gender}
                        required
                        SelectProps={{
                            native: true
                        }}>            
                        {genders.map((gender) => <option key={gender.value} value={gender.value}>{gender.label}</option>)}
                    </TextField>
                </fieldset>
                < PassWordsFieldSet />
                {this.PrivacyProtectionPolicy()}
            </form>
        )
    }

    PrivacyProtectionPolicy () {
        return (
            <div style={{
                display: "grid",
                gridTemplateColumns: "56px 1fr",
                width: "100% !important",
                textAlign:"start"
            }}>
                <Checkbox 
                    className="check"
                    required/>
                <p>I understand and I bind to <a href={this.state.termsOfUseLink}> the Terms of Use </a> of CAREX Services. Also, I understand the <a href={this.state.privacyPolicy}>privacy protection policy</a> provided by CAREX.</p>
            </div>
        )
    }

    handleFeedback = (value: boolean, message: any, severity: any) => {
        if (value) {
            this.setState({
                feedbackMsg: message,
                feedbackSeverity: severity,
                hasFeedback: true
            })
        }
        else {
            this.setState({
                hasFeedback: value
            })
        }
    }

    onSubscriptionSubmit = (e: React.MouseEvent<HTMLButtonElement>) => {
        const form = document.querySelector<HTMLFormElement>(".signUpForm")
        form?.checkValidity()
                
        if (form?.reportValidity()){
            // let date = new Date()
            const role = form?.myrole.value 
            const name = form?.myname.value
            const surname = form?.surname.value 
            const dob = form?.dob.value
            
            // TODO: calculate age before submiting
            // and return if younger
            const phone = form?.phone.value 
            const gender = form?.gender.value
            const password = form?.password.value
            const country = form?.querySelector<HTMLDivElement>(".selected-flag")?.title.split(":")[0]
            const fullname = `${name} ${surname}`

            const data = {
                role: role,
                fullname: fullname,
                dob: dob,
                phone: phone,
                gender: gender, 
                password: password,
                country: country
            }
            // console.log(data)                
            // axios.post(
            //     "/authentication/createCredentials",
            //     JSON.stringify(data),
            //     {
            //         headers : {
            //             "Content-Type": "application/json"
            //         },
            //     }
            // ).then(success => {

            // })
            fetch(
                "/authentication/createCredentials",
                {
                    method: "POST",
                    mode: "cors",
                    headers : {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify(data)
                }
            ).then(response => {

                    if (!response.ok){
                        response.json().then( content => {
                            this.handleFeedback(true, content["response"], "error")
                            console.log(content["response"])
                        })
                        return
                    }
                    response.json().then(
                        data => {
                            this.handleFeedback(true, data["response"], "success")
                            // const public_id = data["public_id"]
                            window.location.href = `/members/practitioners`
                        }
                    )
                    console.log(response.headers.get("access_token"))
                })
            .catch((error) => {
                this.handleFeedback(true, error, "error")
            })
        }
        else {
            return
        }
        
    }

    render(){
        const {message} = this.props
        // this.setState({
        //     signupForm: <this.SignUpForm />
        // })
        return(
            <div>
                <em>{message}</em>
                {this.state.signupForm}
                {
                    this.state.hasFeedback ?
                    <FeedbackBlock 
                        severity={this.state.feedbackSeverity} 
                        message={this.state.feedbackMsg} 
                        closeHandler={this.handleFeedback}
                        open={this.state.hasFeedback}
                        feedref={this.feedbackBlock} /> :
                        null
                }
                <div 
                    style={{
                        display:"flex",
                        alignItems: "flex-start",
                        padding: 16
                    }}>
                    <Button
                        className="subscribeBtn"
                        type="submit" 
                        style={{
                            alignSelf:"flex-end",
                            fontWeight: 900,
                            border: "1px solid lightslategrey",
                            color: "lightslategrey"
                        }}
                        onClick={this.onSubscriptionSubmit}> 
                        SUBSCRIBE 
                    </Button>
                </div>
            </div>
        )
    }
}

const PassWordsFieldSet = (props: any) => {
    const [passwdError, setError] = useState(false)
    const passwdErrorMsg = passwdError ? "Password not compatible" : ""
    // const {message } = props

    const checkPassword = (e: React.ChangeEvent<HTMLInputElement>) => {
        const passwd = document.querySelector<HTMLInputElement>("#password")
        const passvalue: string | undefined = passwd?.value
        const passsize = passvalue!.length

        const value = e.currentTarget.value
        // const valuesize: number | undefined = value.length
        // console.log(passvalue)
        
        if (0 === passsize && value.length > 0){
            setError(true)
            return
        }
        else if ( value!.length >= passsize && value.slice(0, passsize) !== passvalue){
            setError(true)
            return
        } else {
            setError(false)
            return
        } 
    }
 
    const onSetPassword = (e:  React.ChangeEvent<HTMLInputElement>) => {
        // const content = e.currentTarget.value
        // const data = JSON.stringify({
        //     'keytype': 2,
        //     'value': content
        // })
        // fetch(
        //     "/authentication/retrievePublicKeys",
        //     {
        //         method: "POST",
        //         mode: 'cors',
        //         headers: {
        //             ContentType: "application/json; charset=utf-8",
        //             Accept: "application/json"
        //         },
        //         body: data
        //     }
        // ).then(response => {
        //     if (response.ok) {
        //         response.json().then(data => {
        //             console.log(data)
        //         })
        //     }
        // }).catch((reason) => {
        //     console.log(reason)
        // })
    }

    return (
        <fieldset
                className="passwords"
                style={{
                    display: "flex",
                    flexDirection: "column",
                    width:"100%",
                    rowGap: 16,
                    border: "none",
                    padding: 16
                }}
                >
                <TextField
                    type="password" 
                    className="textField password" 
                    name="password" 
                    placeholder="*****************"
                    label="Password"
                    variant="outlined" 
                    id="password"
                    error={passwdError}
                    helperText={passwdErrorMsg}
                    onChange={onSetPassword}
                    required/>
                <TextField
                    type="password" 
                    className="textField passconfirm" 
                    name="passconfirm"
                    placeholder="*****************"
                    label="Confirm password"
                    variant="outlined" 
                    id="passconfirm"
                    required
                    error={passwdError}
                    helperText={passwdErrorMsg}
                    onChange={checkPassword}/>
            </fieldset>
    )
}

export default SignUp;
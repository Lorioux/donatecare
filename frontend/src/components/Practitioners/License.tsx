import { createStyles, FormControl, makeStyles, TextField } from '@material-ui/core'
import React, { Component, useState } from 'react'

const useStyles = makeStyles(() =>
createStyles({
    license: {
        display: "flex",
        flexDirection: "column",
        width: "100%",
        borderTop: "1px solid lightslategrey"
    },
    licenseField : {
        width : "100%"
    }
}))

export function License(props: any) {
    // const date = new Date()
    const [code, setCode] = useState("")
    const [IssueDate, setIssueDate] = useState("")
    const [ValidDate, setValidDate] = useState("")
    const [Issuer, setIssuer] = useState("")
    const [Country, setCountry] = useState("")
    const [Certificate, setCertificate] = useState("")
    // const [DoctorId, setDoctorId] = useState("")
    const {doctorId} = props

    const classes = useStyles()

    const changeLicenseValues = (ev: React.ChangeEvent<HTMLInputElement>) =>{
        const name = ev.currentTarget.name
        switch (name) {
            case "code":
                setCode(ev.target.value)
                break
            case "issuedate":
                setIssueDate(ev.target.value)
                break
            case "validdate" : 
                setValidDate(ev.target.value)
                break 
            case "isser":
                setIssuer(ev.target.value)
                break 
            case "Country":
                setCountry(ev.target.value)
                break
            case "certificate":
                setCertificate(ev.target.value)
                break 
            default:
                break;
        }
    }

    return (
        <FormControl itemID={doctorId}
            className={classes.license}
            >
            <TextField
                className="licenseField"
                name="code"
                value={code}
                onChange={changeLicenseValues}
                label="License code"
                variant="outlined"
                />

            <TextField 
                className="licenseField"
                name="issuedate"
                value={IssueDate}
                onChange={changeLicenseValues}
                label="Issue date"
                variant="outlined"/>

            <TextField 
                className="licenseField"
                name="validdate"
                value={ValidDate}
                onChange={changeLicenseValues}
                label="End Date"
                variant="outlined"/>  

            <TextField 
                className="licenseField"
                name="certificate"
                value={Certificate}
                onChange={changeLicenseValues}
                label="Certificate copy"
                variant="outlined"/>

            <TextField 
                className="licenseField"
                name="issuer"
                value={Issuer}
                onChange={changeLicenseValues}
                label="Issuer name"
                variant="outlined"/>

            <TextField 
                className="licenseField"
                name="country"
                value={Country}
                onChange={changeLicenseValues}
                label="Issuer country"
                variant="outlined"/>    

        </FormControl>
    )
}


export default class Licenses extends Component {
    constructor(props: any) {
        super(props)
    
        this.state = {
           licenses : {}  
        }
    }
    addLicense = () => {
        // TODO: Add new empty license records form

    }
    render() {
        return (
            <div id="licences">
                
            </div>
        )
    }
}


import React, { Component, useState } from 'react'
import { Button, Chip, createStyles, FormControl, Icon, makeStyles, TextField, Typography } from '@material-ui/core'
import AddIcon from "@material-ui/icons/Add"
import { Save } from '@material-ui/icons'
import localForage from "localforage"

const useStyles = makeStyles(() =>
    createStyles({
        license: {
            display: "flex",
            flexDirection: "column",
            width: "100%",
            borderTop: "1px solid lightskyblue",
            rowGap: 24,
            maxWidth: 650,
            marginBottom: 32
        },
        licenseField : {
            width : "100%"
        },  
    }))


localForage.config({
    driver: [localForage.WEBSQL,
                localForage.INDEXEDDB,
                localForage.LOCALSTORAGE],
    name: 'Licences-WebSQL'
});

const storage = localForage.createInstance({
    name : "licences",
    description: `
    Practitioner's licences records
    `
})

export function License(props: any) {
    const date = new Date()
    const month = date.getMonth() < 8 ? `0${date.getMonth()+1}` : `${date.getMonth()+1}`
    const today = `${date.getFullYear()}-${month}-${date.getDate()}`
    const [code, setCode] = useState('')
    const [IssueDate, setIssueDate] = useState(today)
    const [ValidDate, setValidDate] = useState(today)
    const [Issuer, setIssuer] = useState('')
    const [Country, setCountry] = useState('')
    const [Certificate, setCertificate] = useState('')
    // const [DoctorId, setDoctorId] = useState("")
    const {doctorId} = props
    const {removeCallback} = props

    const licenseRecords : Map<number, {
                                code : string,
                                issuedate: string,
                                enddate: string,
                                certificate: Blob | null
                            } > = new Map()

    const saveTemporaryRecords = (record : any) =>{
        // saveChangeCallback(index, {key: "code", value: ev.target.value})
        // const tmp = this.licenseRecords.get(index)
        storage.setItem(indexKey, record)
        console.log("Save control...")
        // const key = record["key"]
        // console.log("caca")
        // switch (key) {
        //     case "code":
        //         licenseRecords!.get(index)!.code = record.get("value")
        //         console.log("caca")
        //         break;
        //     case "issuedate":
        //         licenseRecords!.get(index)!.issuedate = record.get("value")
        //         break;
        //     case "enddate":
        //         licenseRecords!.get(index)!.enddate = record.get("value")
        //         break;
        //     case "certificate":
        //         licenseRecords!.get(index)!.certificate = record.get("value")
        //         break;
        //     default:
        //         break;
        // }
    }

    const {indexKey} = props

    const classes = useStyles()

    const changeLicenseValues = (ev: React.ChangeEvent<HTMLInputElement>) =>{
        const name = ev.currentTarget.name
        switch (name) {
            case "code":
                setCode(ev.target.value)
                saveTemporaryRecords({code: ev.currentTarget.value})
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
            id="license"
            >      
            {
                indexKey > 1 ?                                     
                <Chip
                    // icon={<AddIcon />}
                    label="Remove license"
                    // onDelete={this.addNewLicenseBlock}
                    color= "secondary"
                    style={{
                        margin: 16,
                        width: "max-content"
                    }}
                    onDelete={()=>removeCallback(indexKey)} />
                : <br/>
            }
                
            <TextField
                className="licenseField"
                name="code"
                value={code}
                onChange={changeLicenseValues}
                label="License code"
                variant="outlined"
                required
                />

            <div style={{
                display: "grid",
                gridTemplateColumns: "1fr 1fr",
                columnGap: 16
            }}> 
            <TextField 
                type="date"
                className="licenseField"
                name="issuedate"
                value={IssueDate}
                onChange={changeLicenseValues}
                InputLabelProps={{ shrink: true }}
                label="Issue date"
                variant="outlined"
                required/>

            <TextField
                type="date"
                className="licenseField"
                name="validdate"
                value={ValidDate}
                onChange={changeLicenseValues}
                InputLabelProps={{ shrink: true }}
                label="End Date"
                variant="outlined"
                required/>
            </div>

            <TextField 
                className="licenseField"
                name="certificate"
                value={Certificate}
                onChange={changeLicenseValues}
                label="Certificate copy"
                type="file"
                InputLabelProps={{ shrink: true }}
                variant="outlined"
                required/>

            <TextField 
                className="licenseField"
                name="issuer"
                value={Issuer}
                onChange={changeLicenseValues}
                label="Issuer name"
                variant="outlined"
                required/>

            <TextField 
                className="licenseField"
                name="country"
                value={Country}
                onChange={changeLicenseValues}
                label="Issuer country"
                variant="outlined"
                required/>    

        </FormControl>
    )
}


export default class Licences extends Component<{}, {
    licences: Array<JSX.Element>,
    numOfLicences: number
}> {
    private doctorId: string
    private licences: Map<string, JSX.Element>
    
    constructor(props: any) {
        super(props)
        this.addNewLicenseBlock= this.addNewLicenseBlock.bind(this)
        this.removeLicenseBlock = this.removeLicenseBlock.bind(this)
        this.getAddedLicences = this.getAddedLicences.bind(this)
        this.addLicense = this.addLicense.bind(this)
        this.handleStateChanges = this.handleStateChanges.bind(this)
        this.saveLicenseRecords = this.saveLicenseRecords.bind(this)
        this.retrieveLicenseRecords = this.retrieveLicenseRecords.bind(this)
        // this.handleLicenseRecords = this.handleLicenseRecords.bind(this)
        
        this.doctorId = props.doctorId

        this.licences = new Map()
        this.addLicense(1, this.licences)

        
        
        
        this.state = {
           licences : this.getAddedLicences(),
           numOfLicences : 1
        }

    }
    getAddedLicences(){
        let listOfLicences: Array<JSX.Element> = []
        this.licences.forEach((license, key) => listOfLicences.push(license))
        return listOfLicences
    }

    addLicense(index: any, licences: Map<string, JSX.Element>) {
        const key = `${index}-${this.doctorId}`
        const license = <License 
                            key={`${key}-${this.doctorId}`} 
                            removeCallback={this.removeLicenseBlock} 
                            indexKey={index}/>
  
        this.licences.set(key, license)

        // this.handleLicenseRecords(index, {
        //     code : '',
        //     issuedate: '',
        //     enddate: '',
        //     certificate: null
        // }, "add")
        return license
    }


    addNewLicenseBlock(){
        // TODO: Add new empty license records form
        const licences = Object.assign([], this.state.licences)
        const index = this.state.numOfLicences + 1
        
        const license = this.addLicense(index, this.licences)
        // this.licences.push(<License key={key} removeCallback={this.removeLicenseBlock} indexKey={key}/>)
        licences.push(license)
        this.handleStateChanges(licences, index)
        // handleLicenseRecords(index, {
        //     code : '',
        //     issuedate: '',
        //     enddate: '',
        //     certificate: null
        // }, "add")     
    }

    removeLicenseBlock = (index: number) => {
        
        const key = `${index}-${this.doctorId}`
        
        this.licences.delete(key)
        // console.log(this.licences)  

        let licences: JSX.Element[] = []
        this.licences.forEach((v, k) => {
            licences.push(v)
            // console.log(k)
        })        
        this.handleStateChanges(licences, licences.length)
        // this.handleLicenseRecords(index, null, "delete")
    }
    
    // handleLicenseRecords(index: number, records: any, operation: string){
        
    //     console.info("License record handling")
    //     switch (operation) {
    //         case "add":
    //             this.licenseRecords.set(index, records)
    //             break;
    //         case "remove" : 
    //             this.licenseRecords.delete(index)
    //             break
    //         default:
    //             break;
    //     }
        
    // }

    handleStateChanges(licences: any, numOfLicences: number){
        this.setState({ 
            numOfLicences: numOfLicences,
            licences: licences})
    }

    saveLicenseRecords(){

        
        storage.setItem("Test", "All tests")
        
    }

    retrieveLicenseRecords(){
        let records = []
        this.state.licences.map(license => {
            records.push({
                code : "",
                issuedate : "",
                enddate: "",
                certificate: "",
                isser: "",
                issuercountry: ""
            })
        })
    }

    render() {
        return (   
            <div id="licences"
                style={{
                    width: "100%",
                    display: "flex",
                    flexDirection: "column",
                    alignItems: "center",
                }}>
                <Typography 
                    style={{
                        textAlign: "start",
                        width: 800,
                        padding: 16,
                        borderTop: "1px solid lightslategrey",
                        fontWeight: 700,
                        fontSize: 24,
                        color: "lightslategray"}}>Licences </Typography>
                {
                    this.state.licences.map((license) => (license))
                }
                <div
                    style={{
                        width: 650,
                        display: "flex",
                        flexDirection: "row",
                        marginBottom: 16,
                        columnGap: 16
                    }}>
                    <Chip
                        icon={<AddIcon />}
                        label="ADD ANOTHER"
                        // onDelete={this.addNewLicenseBlock}
                        color="primary"
                        onClick={this.addNewLicenseBlock}
                    />
                    <Chip
                        icon={<Save />}
                        label="SAVE RECORDS"
                        // onDelete={this.addNewLicenseBlock}
                        color= "secondary"
                        onClick={this.saveLicenseRecords}
                    />
                </div>
                
            </div>
        )
    }
}


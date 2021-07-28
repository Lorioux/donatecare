import { createStyles, makeStyles, TextField, Typography } from '@material-ui/core'
import React, { useState } from 'react'
import PhoneInput from 'react-phone-input-2'
import "react-phone-input-2/lib/style.css"

const classes = {
        personalinfo : {
            maxWidth: 700
        },
        phone : {
            maxWidth: "max-content"
        },
        fields : {
            width: "100%",
            // marginBottom: 24
        }
    }

export default function PersonalData(props: any) {
    const [genders, setGenders] = useState([
        {label: "Female", value:"female"},
        {label: "Male", value:"male"},
        {label: "Outro", value:"outro"},
    ])
    const [gender, setGender] = useState(props.gender)
    const [phoneNumber, setPhoneNumber] = useState(props.phone)
    const [photo, setPhoto] = useState(props.phone)
    const [name, setName] = useState(props.name)
    const [surname, setSurname] = useState(props.surname)
    const [taxId, setTaxId] = useState('')
    const [birthday, setBirthday] = useState(props.birthday)
    // const classes = useStyles()

    return (
        <fieldset
            id="personaldata"
            style={{
                width: "100%",
                display: "flex",
                flexDirection: "column",
                borderTop: "1px solid lightskyblue",
                alignItems: "center",
                border: "none",
            }}>
            <Typography 
                    style={{
                        textAlign: "start",
                        width: 800,
                        padding: 16,
                        fontWeight: 700,
                        fontSize: 24,
                        color: "lightslategray"}}>Personal Information </Typography>
            <div 
                style={{
                    display: "flex",
                    flexDirection: "column",
                    width: "100%",
                    rowGap: 24,
                    maxWidth: 650,
                    marginBottom: 32, 
                    borderTop: "1px solid lightskyblue",
                    paddingTop: 32
                }}>
                <TextField
                    style={classes.fields}
                    type="file"
                    name="photo"
                    label="Photo"
                    variant="outlined"
                    required
                    value={photo}
                    InputLabelProps={{ shrink: true }}
                    />

                <TextField
                    style={classes.fields}
                    name="name"
                    label="Name"
                    variant="outlined"
                    required
                    value={name}/>

                <TextField
                    style={classes.fields}
                    name="surname"
                    label="Surname"
                    variant="outlined"
                    required
                    value={surname}/>

                <div style={{
                        display: "flex",
                        flexDirection: "row",
                        columnGap: 16,
                        width: "100%"
                    }}>
                    <TextField
                        style={classes.fields}
                        type="date"
                        name="birthday"
                        label="Birth day"
                        variant="outlined"
                        required
                        value={birthday}
                        InputLabelProps={{
                            shrink: true
                        }}
                        />

                    <TextField
                        style={classes.fields}
                        name="gender"
                        label="Gender"
                        variant="outlined"
                        defaultValue={gender}
                        select
                        required
                        SelectProps={{
                            native: true
                        }}> 
                        {
                            genders.map(g => (<option key={g.value} value={g.value}> {g.label} </option>), genders)
                        }
                    </TextField>
                </div>

                <div  style={{
                    display: "grid",
                    gridTemplateColumns: "max-content auto",
                    columnGap: 16,
                    width: "100%"
                }}>
                    <PhoneInput
                        // inputClass="phone"
                        inputProps={{
                            name:"phone",
                            label:"WhatsApp ID",
                            variant:"outlined",
                            // require:true,
                        }}
                        inputStyle={{
                            width: "max-content",
                            height: 56
                        }}
                        country="pt"
                        value={phoneNumber}
                        />
                    <TextField
                        name="taxnumber"
                        label="Tax ID Number"
                        variant="outlined"/> 
                </div>           
            </div>
        </fieldset>
    )
}

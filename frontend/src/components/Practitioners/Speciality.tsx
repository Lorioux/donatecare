import { TextField, TextareaAutosize, Typography, FormControl} from '@material-ui/core'
import React, { useState } from 'react'

export function Speciality() : JSX.Element {

    return (
        <FormControl
            style={{
                display: "flex",
                flexDirection: "column",
                rowGap: 24,
                width: 650,
                borderTop: "1px solid lightskyblue",
                marginBottom: 32,
                paddingTop: 32
            }}>
            <TextField 
                type="text"
                label="Title"
                variant="outlined"
                required
                />  
            <TextareaAutosize
                maxLength={250}
                rowsMin={10}
                style={{
                    padding: 16
                }}
                placeholder="Description"
                required
                />
        </FormControl>
    )
}

export default function Specilities(props: any) : JSX.Element {
    const {initialIndex} = props
    const addSpecialityBlock = (e: any) => {
          
    }
    const [specialities, setSpecialities] = useState(
                new Map<string, JSX.Element>().set(props.initialIndex, 
                        <Speciality key={initialIndex} />) )
    let specialityNodes = Array<JSX.Element>()

    specialities.forEach((speciality, key) => specialityNodes.push(speciality) )


    return (
        <div
            style={{
                width: "100%",
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                // padding: 32
                marginBottom: 24
            }}>
             <Typography 
                style={{
                    textAlign: "start",
                    width: 800,
                    padding: 16,
                    borderTop: "1px solid lightslategrey",
                    fontWeight: 700,
                        fontSize: 24,
                        color: "lightslategray"
                }}>Specialities</Typography>
            {
                specialityNodes.map(speciality => (speciality))
            }
        </div>
    )
}


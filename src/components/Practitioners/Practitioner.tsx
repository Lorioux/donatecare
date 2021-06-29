import React from "react"
import calender from "./Calender.css"


interface PractitionerState {
    ProfilePhoto: JSX.Element | null ,
    FullName: JSX.Element | string ,
    Speciality: JSX.Element | string ,
    ConsultMode: JSX.Element | string | Array<JSX.Element>,
    Licenses: JSX.Element | string | Array<String> 
    Calender: JSX.Element | string,
    Address: JSX.Element | string,
}

class Practitioner extends React.Component{
    constructor(props){
        super(props)
    }
}

function Calender() {
    const style = {
        
    }
    return (
        <div style={calender}>
            
        </div>
    )
}
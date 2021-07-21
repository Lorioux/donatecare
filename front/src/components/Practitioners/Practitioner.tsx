import React from "react"
import { render } from "react-dom"


import {FontAwesomeIcon} from "@fortawesome/react-fontawesome"
import { faCalendarWeek, faRoute, faVideo } from '@fortawesome/free-solid-svg-icons'

import { Button, createStyles} from "@material-ui/core"


import "./Calendar.css"
import "./Practitioner.css"
import Calendar from "./Calendar"
import Booking from "../Booking/BookNow"

import logo from "../../logo.svg"
import { any, string } from "prop-types"


interface PractitionerState {
    Identification: string,
    ProfilePhoto: JSX.Element | null ,
    FullName: JSX.Element | string ,
    Speciality: JSX.Element | string ,
    ConsultMode: JSX.Element | string | Array<JSX.Element> | {},
    Licenses: JSX.Element | string | Array<String>,
    Calendar: JSX.Element | string | null | {},
    CalendarSlots: {} | null,
    Address: JSX.Element | string,
    RouteMap: JSX.Element | null | string,
    CalendarIco: JSX.Element | null,
    MapIco: JSX.Element | null,
    orientation: string;
    cache: {calendar: JSX.Element | any, route: JSX.Element | any},
    bookingDlg: JSX.Element | null,

}

// const useStyles = makeStyles((theme: Theme) => {
//     createStyles({
//         title: {

//         }
//     })
// })

class Practitioner extends React.Component<{}, PractitionerState>{
    id: Number
    constructor(props: any){
        super(props)
        this.id = props.id
        const slots = [
            "08:00", "09:00", "10:00",
            "11:00", "12:00", "13:00",
            "14:00", "15:00", "16:00"
        ]

        this.state = {
            Identification: "",
            ProfilePhoto: null ,
            FullName: "JSX.Element | string" ,
            Speciality: "JSX.Element | string" ,
            ConsultMode: "JSX.Element | string | Array<JSX.Element>",
            Licenses: "JSX.Element | string | Array<String>",
            CalendarSlots: {
                mon: slots,
                tue: slots,
                wed: slots,
                thu: slots,
                fri: slots,
                sat: slots,
                sun: slots,
            },
            Calendar: null,
            Address: "JSX.Element | string",
            RouteMap: null,
            CalendarIco: null,
            MapIco: null,
            orientation: "row",
            cache: {calendar: null, route: null },
            bookingDlg: null,

        }

        this.onCalendarIcoClick = this.onCalendarIcoClick.bind(this)
        this.onRouteIcoClick = this.onRouteIcoClick.bind(this)
        this.handleCalendarAndRouteDisplay = this.handleCalendarAndRouteDisplay.bind(this)
    
    }

    render(){
        let vCards: JSX.Element[] = []
        let e = {'speciality': 'Nutrition', 'location': 'Lisbon'}
        SearchPractitioners(e).forEach( (card : PractitionerState, index: Number) => 
            vCards.push(<Practitioner data-info={card} key={card.Identification} /> )
        )
        const mainInfo = (
            <div className="mainBlock">
                <div className="photoFullname">
                    <img src={logo} className="photo" alt="profile_photo"/>
                    <span className="fullnameArea">
                        <em className="fullname">Onchologist</em>
                        <h4 className="fullname">Dr. John Doe</h4>
                    </span>
                </div>
                <div className="modeArea">
                    <FontAwesomeIcon icon={faVideo}  className="IcoCol"/>
                    <div className="modeName">
                        <em>Video Consultation</em>
                        <span className="moreBtn">MORE</span>
                    </div>
                </div>
            </div>
        )

        const HandleBooking = (e: any)=>{
            this.setState({bookingDlg: null})
            const  booking = <Booking 
                                Open={true} 
                                DoctorFullname="Dr. John Doe"
                                DoctorIdentification="Av.  Carolina Michaelis 49"
                                DoctorSpeciality="Nutritionist"
                                ConsultationDate={new Date()}
                                BeneficiaryFullName="string"
                                BeneficiaryFiscalIdentityNumber="string" />
            
            this.setState({bookingDlg: booking})            
        }

        const licenseInfo = (
            <div className="licenseBlock">
                <div style={{display: "flex",  
                        flexDirection: "row", 
                        justifyContent: "left", 
                        columnGap: 16, 
                        marginTop: 16}}>
                    <Button
                        style={{
                            backgroundColor: "lightskyblue",
                            fontWeight: 700,
                            color: "lightslategray"
                        }}
                        onClick={(e) => HandleBooking(e)}>
                        BOOK NOW
                    </Button>    
                    <FontAwesomeIcon 
                        icon={faCalendarWeek} 
                        className="calenderIco" 
                        style={{
                            width: 26 , height: 26
                        }} onClick={(e) => this.onCalendarIcoClick(e)} />
                    <FontAwesomeIcon 
                        icon={faRoute} 
                        className="routeIco" 
                        style={{
                            width: 26 , height: 26
                        }}
                        onClick={(e) => this.onRouteIcoClick(e)} />
        
                </div>
                <div className="addressInfoArea">
                    <h5 
                        style={{
                            marginTop: 4
                        }}>Address:</h5>
                    <span className="addressInfo">Av. Carolina Michaelis 49, Lisbon, PT</span>
                </div>
                <div className="licenseArea">
                    <h5 
                        style={{
                            marginTop: 4,
                        }}>Licenses:</h5>
                    <span className="licenseCode">CC22000CSS</span>
                </div>
            </div>
        )

        return(
            <div key="1">
                <div className="practitionersCard">
                    <div className="practitionerInfo">
                        {mainInfo}
                        {licenseInfo}
                    </div>
                    <div className="calendar-routeArea">
                        {this.state.Calendar}
                        {this.state.RouteMap}
                    </div>
                </div>
               <div className="bookingDlgArea" key="2">
                    {this.state.bookingDlg}
                </div> 
            </div>
        )
    }

    currentOrientation(){
        const width = window.screen.width;
        if (width<= 720){
            this.setState({
                orientation: "column",
            })
        } else {
            this.setState({
                orientation: "row"
            })
        }
    }

    changeState = (state: string | {}, e: any) => {
        if (state instanceof string){
            this.setState({
                Calendar: e
            })
        } else if (state instanceof any){
            for(var s in state) {
                var v = `${s}`
                switch (s) {
                    case "Calendar" :
                        this.setState({ Calendar: v })
                        break;
                    case "RouteMap":
                        break;
                    default:
                        break;
                }
            }
        }
    }

    handleCalendarAndRouteDisplay(e: any){
        var orientation = this.currentOrientation()
        if ( "column" === `${orientation}` ){
            render(
                e,
                document.getElementsByClassName('calendarArea')[0]
            )
        }
    }

    onCalendarIcoClick(e: any){

        const date = ""
        console.log(date)
        // If calender is visible the dismiss. Otherwise, show calender
        const changeState = (e: any) =>{
            this.setState({Calendar: e})
        }
        
        if (this.state.Calendar !== null) {
            this.setState(
                (state) => {state.cache.calendar = this.state.Calendar}
            )
            
            changeState(null)
        }        
        else {
            if (this.state.RouteMap !== null ){
                
                this.setState((state) => { state.cache.route = this.state.RouteMap})
                this.setState({RouteMap : null})
                // console.log(1)
            }
            // Keep the calendar into cache state
            if (this.state.cache.calendar !== null){
                changeState(this.state.cache.calendar)
            }
            else {
                changeState(<Calendar data-slots={this.state.CalendarSlots} />)
            }
        }
        //console.log(this.state.cache)
        // this.handleCalendarAndRouteDisplay(this.state.Calendar)
    }

    onRouteIcoClick(e: any){
        const changeState = (e: any) =>{   
            this.setState({RouteMap: e})
        }
       
        if (this.state.RouteMap !== null ){
            this.setState((state) => { state.cache.route = this.state.RouteMap})
            changeState(null)
        }
        
        else {

            if (this.state.Calendar !== null ){
                this.setState((state) => { state.cache.calendar = this.state.Calendar})
                this.setState({Calendar: null})
            }
            // Keep the route into cache state
            if (this.state.cache.route !== null){
                changeState(this.state.cache.route)
            }
            else {
                changeState("TEST")
                this.setState((state) => { state.cache.route = "TEST_FROM_CACHE"})
            }
            
        }
        //console.log(this.state.cache)
        // this.handleCalendarAndRouteDisplay(this.state.RouteMap)
    }

}

const SearchPractitioners = (e: any) : [] => {
    let speciality = e['speciality']
    let location = e['location']
    let url = `/members/doctors?speciality=${speciality}&location=${location}`
    
    fetch(url, {
        method: "GET",
        mode: "cors",
        credentials: "same-origin",
        headers: {
            contentType: "application/json",
        },
        redirect: "follow",
        referrerPolicy: "origin"}).then( response => response.json().then( data => {
            console.log(data)
        }

        ))
    return []
}

export const Practitioners = (e: any): JSX.Element[] => {
    // let useStyles = createStyles({
    //     content : {
    //         width: "100%",
    //         Height: "max-content"
    //     }
    // })
    // start search 
    let vCards: JSX.Element[] = []
    SearchPractitioners(e).forEach( (card : PractitionerState, index: Number) => 
        vCards.push(<Practitioner data-info={card} key={card.Identification} /> )
    )

    return vCards
}




export default Practitioner
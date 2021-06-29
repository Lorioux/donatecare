import React from "react" 
import "./FrontDesk.css"
import logo from "../../logo.svg"
import { render } from "react-dom"


interface FrontDeskState {
    searchBlock: JSX.Element | null,
    availablePractitioners: JSX.Element | null | JSX.Element[],
    promotionBlock: JSX.Element | string | null,
    testimonial: JSX.Element | null,
    locatins: JSX.Element | null, 
}
class FrontDesk extends React.Component<{}, FrontDeskState> {
    constructor(props: any){
        super(props)
        this.state = {
            searchBlock: null, // SearchBlock(),
            availablePractitioners: this.AvailablePractioners(),
            promotionBlock: null,
            testimonial: null,
            locatins: null,
        }

        SearchBlock.bind(this)
        this.AvailablePractioners = this.AvailablePractioners.bind(this)
    }
    render(){
        return(
            <div style={{
                margin: 36
            }}>
                {this.state.searchBlock}
                {this.state.availablePractitioners}
            </div>
        )
    }

    AvailablePractioners() {
        
        const practitioner = (
            <div className="practitionerCard">
                   
            <div id="cardDetails" className="cardDetails">
                 <img  id="practitionerPhoto" src={logo} ></img>
                 <div className="practitionerSummary">
                    <h5 id="practitionerName" style={{margin: 0}}>Dr. John Doe</h5>
                    <span id="practitionerSpec">Opthalmologist</span>
                    <div className="consulMode">
                        {/* <button>Book now</button> */}
                        <em>Video call</em>
                        {" | "}
                        <em>Presential</em>
                        {" | "}
                        <em style={{backgroundColor: "lightskyblue"}}>Free</em>
                    </div>
                 </div>

            </div>
            </div>
        )
        // this.setState({availablePractitioners: [practitioner, practitioner, practitioner]})
        // console.log(this.state.availablePractitioners)
        window.addEventListener("load", () => {
            let list = []
            for(let i=0; i < 9; i++){
                list.push(practitioner)
            }
            render(
                list,
                document.getElementById("practititonersList")
            )
        })
        return(
            <div className="availabilityGrid"
                style={{
                    color: "lightslategray",
                    justifyContent: "center",
                    margin: "36px 8px 36px",
                }}>
                <span style={{borderBottom: "1px solid lightblue", fontWeight: 900, fontFamily: "Ubuntu", fontSize: 36}}>We care for free: </span>
            <div id="practititonersList"
                style={{
                    display: "flex",
                    flexWrap: "wrap",
                    margin: 16,
                    justifyContent: "center",
                }}>
                   {/* {practitioner} {practitioner} {practitioner} {practitioner} */}
            </div>
            </div>
        )
    }
}

export function SearchBlock() {
    return(
        <div style={{
            width: "100% !import",
            display: "flex",
            flexDirection: "column",
            justifyContent: "center",
            backgroundColor: "lightslategray",
            color: "whitesmoke",
            marginBottom: 16,
            padding: 48,
        }}
        className="searchBlock">
            <h3> Find and book your physician, anytime. </h3>
            <form className="searchForm">
                <input 
                    style={{margin: 10,}}
                    type="text" name="speciality" placeholder="Speciality" />
                <input  style={{margin: 10, }} type="text" name="location" placeholder="Location"/>
                <input type="submit" className="searchBtn" style={{
                    backgroundColor: "lightslategray", margin: 10, height: 52, width: "fit-content", padding: 6, color: "whitesmoke"
                }} value="SEARCH" />

            </form>
        </div>
    )
}

export function CallForAction() {
    let style = {
        display: 'flex',
        flexDirection: 'column',
        position: 'fixed',
        left: 4,
        top: "50%",
        color: 'skyblue',
        fontWeight: 900,
        backgroundColor: "transparent",
    }
    let action = {
        writingMode: 'vertical-lr',
        textOrientation: 'upright',
        border: '1px solid lightslategray',
        borderRadius: '4px',
        width: "36px",
        padding: "4px"
    }
    const callActions = (
        <div style={style}>
            <i id="subscribe" style={action} onClick={(e)=> onClick(e)} >SUBSCRIBE</i>
            <hr/>
            <i id="donate" style={action} onClick={(e)=> onClick(e)}>DONATE</i>
        </div>
    )
    const onClick = (e: any) =>{
        if (e.target.id == "subscribe") window.location.href="/subscribe"
        if (e.target.id == "donate") window.location.href="/donate"
    }


    return(callActions)
}

export default FrontDesk
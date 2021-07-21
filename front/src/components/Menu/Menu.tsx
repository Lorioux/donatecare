import React from "react"
import ReactDOM from "react-dom"

import SignIn from "../Members/SignIn"
import Memebrs from "../Members/Members"
import { CallForAction } from '../Home/FrontDesk'
import Donate from "../Donating/DonateNow"

import { FontAwesomeIcon } from "@fortawesome/react-fontawesome"
import { faStethoscope, faUnlock, faRobot } from "@fortawesome/free-solid-svg-icons"

import './Menu.css'

interface MenuState {
    actionsVisibility: boolean
    actions: JSX.Element | null,
    orientation: string | string,
    menuIcon: JSX.Element | null,
    subscribe: JSX.Element | null,
    donate: JSX.Element | null
}

class Menu extends React.Component<{}, MenuState> {
    ActionsVisibility = true
    
    constructor(props: any){
        super(props)
        this.ActionsVisibility = true
        this.state = {
            actionsVisibility: true, // When set True it is drawn (Veritally|Horizontally). Otherwise, an Icon(Collapsed)  will be shown            
            orientation: this.Orientation(),
            actions:  this.MenuActions(),
            menuIcon: this.MenuIcon(),
            subscribe: null,
            donate: null
        }
        this.MenuLoadHandler = this.MenuLoadHandler.bind(this)
        this.MenuIcon = this.MenuIcon.bind(this)
        this.WindowResizeHandler = this.WindowResizeHandler.bind(this)
        this.MenuActions = this.MenuActions.bind(this)
        this.onMenuIconClick = this.onMenuIconClick.bind(this)
        this.menuActionsClose = this.menuActionsClose.bind(this)
        this.menuActionsDisplay = this.menuActionsDisplay.bind(this)
        this.displaySignInUI = this.displaySignInUI.bind(this)
        this.SignInUpLinks = this.SignInUpLinks.bind(this)

        
        window.addEventListener('resize', this.WindowResizeHandler)
    }

    render() {
        window.addEventListener("load", this.MenuLoadHandler)
        return (
            <div className="menuBlock">
                <h1 className="logo" style={{
                        color: "lightskyblue"
                    }}
                    onClick={()=>{window.location.href = "/"}}
                >
                        DONATE CARE
                </h1>
                <menu className="menu">
                    
                    {this.state.actions}
                    {this.state.menuIcon}
                    
                    {/* {this.state.subscribe} */}
                </menu>
            </div>
        )
    }

    WindowResizeHandler(){
        // var width = window.visualViewport.width
        this.setState({
                orientation: this.Orientation()
            })
        this.MenuLoadHandler() 
    }

    MenuIcon = () => {
        this.setState({
            actions: null
        })
        return(
            <i className="menuIcon" onClick={(e)=> this.onMenuIconClick(e)}>MENU</i>
        )
    }

    Orientation = () => { 
        var width = window.document.body.clientWidth
        if (width >= 600 ){
            return "horizontal"
        }
        else {
            this.setState({
                subscribe: CallForAction()
            })
            return "vertical"
            
        }
    } 

    MenuLoadHandler() {
        
        if (this.state.orientation === "vertical"){
            this.setState({
                menuIcon: this.MenuIcon(),
                actionsVisibility: false
            })
        } else {
            this.setState({
                actionsVisibility: true,
                actions: this.MenuActions()
            })
        }
    }

    MenuActions(){
        
        this.setState({
            menuIcon: null,
        })
        const showDonationForm = () => {
            ReactDOM.render(<Donate open={true} />, document.querySelector("main"))
        }
        return (
            <div className="menuActions" style={{color: "whitesmoke"}}> 
                <span className="demoCall menuAction" 
                    onClick={showDonationForm}
                    >
                    <i><FontAwesomeIcon icon={faStethoscope} style={{
                        color: "whitesmoke", marginRight: 2
                    }}/>
                    <em><strong>Doctor?</strong></em></i>
                    <i style={{marginLeft:"2px", fontSize: 14}}>Donate your time</i>
                </span>
                <span className="guideLines menuAction">
                    <FontAwesomeIcon icon={faRobot} style={{
                        color: "whitesmoke", marginRight: 2
                    }}/>
                    Health <i>Guides</i>
                </span>
                <this.SignInUpLinks /> 
                <span className="menuCloseAction menuAction"
                    onClick={(e)=> this.menuActionsClose()}
                >CLOSE</span>
            </div>
        )
    }

    SignInUpLinks(){
        // eslint-disable-next-line
        const joinus = (
            <span className="signUpAction menuAction"
                style={{
                    backgroundColor: "lightblue",
                }}>

                <a href="joinUs"><em><strong>JOIN US</strong></em></a>
            </span>
        )
        return(
            <span className="signInAction menuAction">
                <FontAwesomeIcon icon={faUnlock} style={{
                    color: "whitesmoke",
                    marginRight: 4
                }} />
                <em>SignIn</em>                
            </span>
        )
    }

    onMenuIconClick(e: any){
        
        this.setState({
            actions: this.MenuActions(),
        })
    }
    
    menuActionsDisplay(icon: any){
        let parent = icon.parentNode
        
        var actions = this.MenuActions()
        
        
        if (parent.actions instanceof HTMLDivElement){
            console.log(parent.actions)
            parent.append(parent.actions)
        }
        else {
            this.setState({ actions : actions })
        }

        // hold icon clone and remove element from dom tree.
        parent.icon = icon
        icon.remove()
        console.log(parent)
    }

    menuActionsClose = () => {
        this.setState({
            menuIcon: this.MenuIcon(),
            actionsVisibility: false
        })
        
    }

    displaySignInUI(e: any) {
        var  mainNode = window.document.getElementsByTagName("main")[0]
        console.log(mainNode)
        // mainNode.innerHTML = <SignIn /> 
        this.menuActionsClose() 
        ReactDOM.render(
            <SignIn />,
            mainNode
        )    
    }

    displayMembersUI(){
        ReactDOM.render(
            < Memebrs />,
            document.getElementById("main")
        )
    }
}


export default Menu
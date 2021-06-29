import React, { useState } from "react"
import { render } from "react-dom"
import ReactDOM from "react-dom"

import SignIn from "../Members/SignIn"
import Memebrs from "../Members/Members"

import './Menu.css'

interface MenuState {
    actionsVisibility: boolean
    actions: JSX.Element | null,
    orientation: string | string,
    menuIcon: JSX.Element | null
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
            menuIcon: this.MenuIcon()
        }
        this.MenuLoadHandler = this.MenuLoadHandler.bind(this),
        this.MenuIcon = this.MenuIcon.bind(this)
        this.WindowResizeHandler = this.WindowResizeHandler.bind(this)
        this.MenuActions = this.MenuActions.bind(this)
        this.onMenuIconClick = this.onMenuIconClick.bind(this)
        this.menuActionsClose = this.menuActionsClose.bind(this)
        this.menuActionsDisplay = this.menuActionsDisplay.bind(this)
        this.displaySignInUI = this.displaySignInUI.bind(this)

        window.addEventListener("load", this.MenuLoadHandler)
        window.addEventListener('resize', this.WindowResizeHandler)
    }

    render() {
        return (
            <div className="menuBlock">
                <h1 className="logo" style={{
                        color: "skyblue"
                    }}
                    onClick={()=>{window.location.href = "/"}}
                >
                        DONATE CARE
                </h1>
                <menu className="menu">
                    
                    {this.state.actions}
                    {this.state.menuIcon}
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
        var width = window.screen.width
        if (600 <= width  ){
            return "horizontal"
        }
        else {
            return "vertical"
        }
    } 

    MenuLoadHandler() {
        if (this.state.orientation == "vertical"){
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
        
        var direction = "row"
        
        if (window.screen.width  < 600){
            direction = "column"   
        }
        
        this.setState({
            menuIcon: null,
        })
        
        return (
            <div className="menuActions" style={{color: "whitesmoke"}}> 
                <span className="demoCall menuAction">
                    <em><strong>Doctor?</strong></em>
                    <i style={{marginLeft:"2px"}}>Try for free</i>
                </span>
                <span className="guideLines menuAction">Health <i>Guides</i></span>
                <this.SignInUpLinks /> 
                
                <span className="menuCloseAction menuAction"
                    onClick={(e)=> this.menuActionsClose()}
                >CLOSE</span>
            </div>
        )
    }

    SignInUpLinks(){
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
        var style = {
            "visibility": "visible"
        }
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
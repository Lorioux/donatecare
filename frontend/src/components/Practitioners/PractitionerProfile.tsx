import { Paper, Tabs, Tab, Chip, Button, Divider } from '@material-ui/core'
import React, { Component } from 'react'
import Licences from './License'
import PersonalData from './PersonalData'
import Specialities from './Speciality'
import EditIcon from "@material-ui/icons/Edit"



export default class PractitionerProfile extends Component<{}, {
    panelContent: JSX.Element | null
    tabindex: number
}> {

    constructor(props:any) {
        super(props)
        this.getProfilePanel = this.getProfilePanel.bind(this)
        this.TabPanel = this.TabPanel.bind(this)
        this.handleTabClicks = this.handleTabClicks.bind(this)
        this.changeStatus = this.changeStatus.bind(this)

        
        this.state = {
            panelContent: this.getProfilePanel(),
            tabindex: 0
        }

        
    }


    TabPanel = (ppros: any) => {
        return (
            <div>
                { this.state.panelContent}
            </div>
        )
    }

    handleTabClicks = (ev: any) => {
        const key = ev.currentTarget.id 
        switch (key) {
            case "personalinfo" :
                this.setState({ panelContent: this.getProfilePanel()})
                break;
            // case "licences":
            //     this.setState({panelContent: <Licences />})
            //     break;
            // case "specialities":
            //     this.setState({panelContent: <Specialities />})
            //     break;
            default:
                break;
        }
    }

    changeStatus = (e: React.ChangeEvent<{}>, tabNumber: number) => {
        this.setState({
            tabindex: tabNumber
        })
    }


    getProfilePanel(){
        return (
            <form
                style={{
                    borderTop: "1px solid lightskyblue",
                    paddingTop: 16, 
                }}>
                <Chip
                    icon={<EditIcon />}
                    label="Edit profile"
                    color="primary"
                    variant="outlined"
                />
                <PersonalData />
                <Specialities initialIndex={1}/>
                <Licences />
                <Divider/>
                <Button
                    type="submit"
                    style={{
                        border: "1px solid lightslategrey",
                        margin: 32,
                    }}>SAVE CHANGES</Button>
            </form>
        )
    }

    render() {
        return (
            <Paper 
                style={{
                    flexGrow: 1
                }}
                >
                <Tabs
                    value={this.state.tabindex}
                    onChange={this.changeStatus}
                    centered
                    style={{
                        border: 1,
                        borderBottomColor: "lightslategray",
                        paddingTop: 24,
                    }}>
                    <Tab
                        id="personalinfo"
                        label="Profile"
                        style={{
                            fontWeight: 700,
                        }}/>
                    
                    <Tab
                        id="schedules"
                        label="Schedules"
                        disabled
                        />

                    <Tab
                        id="appointments"
                        label="appointments"
                        disabled
                        />          
                </Tabs>
                <this.TabPanel />
                {/* <Licences /> */}
            </Paper>
            // <Licences />
        )
    }
}

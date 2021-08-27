import React from 'react'
import {BrowserRouter as Router, Switch, Route} from "react-router-dom"

// import logo from './logo.svg'
import './App.css'
import Menu from './components/Menu/Menu'
import Members from './components/Authentication/Members'
import FrontDesk, {CallForAction } from './components/Home/FrontDesk'
import SearchBlock from "./components/Searching/Search"
import Practitioner from './components/Practitioners/Practitioner'
import PractitionerProfile from './components/Practitioners/PractitionerProfile'

// import Footer from './components/Footer/Footer'

const App = () => {
  
  return (
    <div className="App">
      <header className="App-header">
      <Menu />  
        {/* <img src={logo} className="App-logo" alt="logo" />
        <p>Hello Vite + React!</p>
        */}
      < SearchBlock />
                
      </header>
      <CallForAction />
      <main id="main" className="App-content">
        
        <React.Fragment>
          <Router>
          <Switch>
            <Route exact path="/" component={FrontDesk} />
            <Route exact path="/subscribe" component={Members} />
            <Route exact path="/members/Authentication" component={Members} />
            <Route exact path="/donate" component={Members} />
            <Route exact path="/tryforfree" component={Members} />
            <Route exact path="/practitioners" component={Practitioner} />
            <Route exact path="/members/practitioners" component={PractitionerProfile} />
          </Switch>
          </Router>
        </React.Fragment>
      </main>
      <div className="App-sidebar"></div>
      {/* <footer className="App-footer">
        <Footer ></Footer>
      </footer> */}
    </div>
  )
}

export default App

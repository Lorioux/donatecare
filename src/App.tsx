import React, { useState } from 'react'
import {BrowserRouter as Router, Switch, Link,  Route} from "react-router-dom"

// import logo from './logo.svg'
import './App.css'
import Menu from './components/Menu/Menu'
// import SignIn from './components/Members/SignIn'
// import FrontDesk from './components/Home/FrontDesk'
import Members from './components/Members/Members'
import FrontDesk, { SearchBlock, CallForAction } from './components/Home/FrontDesk'

import Footer from './components/Footer/Footer'

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
            <Route exact path="/joinUs" component={Members} />
              
          </Switch>
          </Router>
        </React.Fragment>
      </main>
      <div className="App-sidebar"></div>
      <footer className="App-footer">

      </footer>
    </div>
  )
}

export default App

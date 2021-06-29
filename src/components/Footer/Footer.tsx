import React from "react"
import {render} from "react-dom"


interface FootState {
    MessageChannel: JSX.Element | null,
    PostInfo: JSX.Element | null
}

class Footer extends React.Component<{}, FootState> {
    constructor(props){
        super(props)

        this.state = {
            MessageChannel: this.Messaging() ,
            PostInfo: this.Posting()
        }

        this.Messaging = this.Messaging.bind(this)
        this.Posting = this.Posting.bind(this)
    }

    render(){
        return[
            <div>
                {this.state.MessageChannel}
                {this.state.PostInfo}
            </div>,
            <span><i className="fa fa-copyright" aria-hidden="true">DONATECARE, LLC. 2020</i>{" | "} All rights reserved.</span>
        ]
    }

    Messaging() {

        return(
            <section>
                <span>MESSAGE US</span>
                <form style={{display: "flex", flexDirection: "column", flexBasis: 36}}>
                
                    <input type="text" placeholder="Your first and last name here" required={true} />
                    <input type="email" placeholder="Your email here" required={true}/>
                    <input type="text" placeholder="Subject here" required={true} />
                    <textarea placeholder="Your message here"  required={true} style={{height: "minmax(128px, 1fr)"}}/>
                    <input type="submit" value="SEND" />
                </form>
            </section>
            
        )
    
    }
    
    Posting(){
        return(
            <section>
                <span>CALL US</span>
                <span>Donate Care, LLC.</span>
                <span>Av. Carolina Michaelis, 42</span>
                <span>Oeiras, Linda-a-velha,  2795-050</span>
                <span>Lisbon, PT</span>
                <span>Tel: 00351 920 000 000</span>
                <span>Email: care@donate.care</span>
            </section>
        )
    }
}

export default Footer
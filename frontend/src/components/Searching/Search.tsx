import React from "react"

const SearchBlock = () => {
    
    // eslint-disable-next-line
    const specialities = () => {

    }
    return(
        <div style={{
            width: "100% !import",
            display: "flex",
            flexDirection: "column",
            justifyContent: "center",
            backgroundColor: "lightslategray",
            color: "whitesmoke",
        }}

        className="searchBlock">
            <h3> Find and book your physician, anytime. </h3>
            <div style={{
                display: "flex",
                flexDirection: "row",
                width: "100%",
                justifyContent: "center"
            }}>
                <form className="searchForm" action="/practitioners">
                <input 
                    style={{margin: 10,}}
                    type="text" name="speciality" placeholder="Speciality" list="specialities"/>
                <datalist id="specialities">
                    <option value="Onchologist"></option>
                    <option value="Pediatrician"></option>
                    <option value="Nutrician"></option>
                </datalist>
                
                <input  style={{margin: 10, }} type="text" name="location" placeholder="Location" list="cities"/>
                <datalist id="cities">
                    <option value="Lisbon"></option>
                    <option value="Paris"></option>
                    <option value="Johannesburg"></option>
                </datalist>


                <input type="submit" 
                    className="searchBtn" 
                    style={{
                        backgroundColor: "lightslategray", 
                        margin: 10, height: 52, width: "fit-content", 
                        padding: 6, color: "whitesmoke"
                    }} onClick={(e) => {}}
                
                value="SEARCH" />

            </form>
            </div>
        </div>
    )
}

export default SearchBlock
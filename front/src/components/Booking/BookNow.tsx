import React, { useState } from "react"

import { AppBar, 
        Button, Dialog, DialogContent,
         IconButton, 
        Slide, 
        TextField, 
        Toolbar, Typography } from "@material-ui/core"
import { createStyles, makeStyles, Theme } from "@material-ui/core/styles"
import CloseIcon from "@material-ui/icons/Close"

import { TransitionProps } from '@material-ui/core/transitions';

// eslint-disable-next-line
interface BookNowState {
    DoctorIdentification: string,
    DoctorFullname: string,
    DoctorSpeciality: string,
    ConsultationDate: Date,
    BeneficiaryFullName: string,
    BeneficiaryFiscalIdentification: string,
    // Display: boolean
}

/**
 * TODO: Set Doctors automatically when crating the Interface
 * TODO: Request user Information if NOT logged in.
 * TODO: Redirect user to subscription Page to complete process IF is NOT subscribed YET.
 */

 interface BookingProps {
    DoctorIdentification: string,
    DoctorFullname: string,
    DoctorSpeciality: string,
    ConsultationDate: Date | string,
    BeneficiaryFullName: string,
    BeneficiaryFiscalIdentityNumber: string,
    Open: boolean,
}

function Booking(props: BookingProps){
    // constructor() {
    // }
    const [modelOpen, setOpen] = useState(props.Open)
    
    // eslint-disable-next-line
    const handleClose = () =>{
        setOpen(false)
    }
    // eslint-disable-next-line
    function checkIsUserSubscribed(e: any){
        // TODO: Take users FullName and FiscalIdentification to Validate its autheticity. 
        // Otherwise, redirect to Subscriptions page. 
        return true
    }
    // eslint-disable-next-line
    function redirectToSubscriptions(e: any){

    }
    // eslint-disable-next-line
    function checkIsUserLoggedIn(){
        // TODO: get this session Token and validate 
        return true
    }
    
    // eslint-disable-next-line
    function makeAppointment(e: any){
        // send the request to make appointmant
        // If response a redirect to subscribe, then call redirect 
    }
    // render(<BookingDialog open={modelOpen} />, document.querySelector(".bookingDlgArea"))
    return( <BookingDialog open={modelOpen} data={props}/> )
    
}

const useStyles = makeStyles((theme: Theme) =>
  createStyles({
    appBar: {
      position: 'relative',
      backgroundColor: "lightslategray", 
    },
    title: {
      marginLeft: theme.spacing(2),
      flex: 1,
    },
    textFields:{
        width: "100%",
        marginTop: 20,
    },
    dateTime :{
        display: 'grid',
        gridTemplateColumns: '1fr 1fr',
        columnGap: 16,
        marginTop: 20,
    }
    ,
    content: {
        padding: 36
    }
  }),
);

const Transition = React.forwardRef(function Transition(
  props: TransitionProps & { children?: React.ReactElement },
  ref: React.Ref<unknown>,
) {
  return <Slide direction="up" ref={ref} {...props} />;
});

function BookingDialog(props: any) {
    const classes = useStyles()
    const [open, setOpen] = React.useState(props.open)
    const data = props.data
//   const handleClickOpen = () => {
//     setOpen(true);
//   };

  const handleClose = () => {
    setOpen(false);
  };

  return (
        
    <Dialog open={open} onClose={handleClose} TransitionComponent={Transition}>
        <AppBar className={classes.appBar}>
            <Toolbar>
                <IconButton edge="start" color="inherit" onClick={handleClose} aria-label="close">
                    <CloseIcon />
                </IconButton>
                <Typography variant="h6" className={classes.title}>
                    Booking Ticket
                </Typography>
                <Button autoFocus color="inherit" onClick={handleClose}>
                    Confirm
                </Button>
            </Toolbar>
        </AppBar>
        
        <DialogContent className={classes.content}>
            <form >
            <TextField placeholder={data.DoctorFullname} 
                className={classes.textFields} 
                label="Doctor" 
                variant="outlined" 
                value={data.DoctorFullname} disabled required/>
            <TextField placeholder="Speciality" 
                value={data.DoctorSpeciality}
                className={classes.textFields} 
                label="Speciality" 
                variant="outlined" disabled required/>
            <TextField placeholder="Av. Caroolina Michaelis 45" 
                className={classes.textFields} 
                label="Address line" 
                variant="outlined" required/>
            <div className={classes.dateTime} >
                <TextField type="date" 
                    label="Date"
                    variant="outlined" required/>
                <TextField type="time" 
                    label="Time" 
                    variant="outlined" required/>
            </div> 
            
            <TextField placeholder="Your Full Name" 
                className={classes.textFields} 
                label="My name" 
                variant="outlined" required/>
            <TextField placeholder="Your Fiscal Identity Number" 
                name="fiscalIdNumber"
                className={classes.textFields} 
                label="Phone Number" 
                variant="outlined" required/>
            <TextField placeholder="Your Fiscal Identity Number" 
                name="fiscalIdNumber"
                className={classes.textFields} 
                label="Fiscal ID Number" 
                variant="outlined" required />
            </form>
            
        </DialogContent>
    </Dialog>

  );
}

export default Booking



export default function validate(state) {

    var validation = {
        password: { error: false, message: '' },
        confirm: { error: false, message: '' },
        fname: { error: false, message: '' },
        lname: { error: false, message: '' },
        email: { error: false, message: '' },
        uname: { error: false, message: '' },
        address: { error: false, message: '' },
    }


    if (!(/\d/.test(state.password) && /[a-z]/.test(state.password) && /[A-Z]/.test(state.password))) {
        validation.password = { error: true, message: 'Passwords must contain at least one lowercase, one uppercase and one digit' }
    }

    if (state.password.length < 8) {
        validation.password = { error: true, message: 'Passwords must be at least 8 characters' }
    }

    if (state.confirm !== state.password) {
        validation.confirm = { error: true, message: 'Passwords must match' }
    }

    if (state.fname === '') {
        validation.fname = { error: true, message: 'Required' }
    }

    if (state.lname === '') {
        validation.lname = { error: true, message: 'Required' }
    }

    if (!(/^[\w-.]+@([\w-]+\.)+[\w-]{2,4}$/g.test(state.email))) {
        validation.email = { error: true, message: 'Please enter a valid mail address' }
    }

    if (state.uname === '') {
        validation.uname = { error: true, message: 'Required' }
    }

    if (state.address === '') {
        validation.address = { error: true, message: 'Required' }
    }
    
    return validation
}
// Profile Page

function Profile(){
    // Return Profile conatiner
    return (
        <div id="profile_page" class="page">
            <span>Profile</span>
        </div>
    );
}

// Render All Posts page to the DOM
ReactDOM.render(<Profile />, document.querySelector('#profile_wrapper'));

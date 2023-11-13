function displayText() {
    var nickname = document.getElementById("inputRID").value;
    console.log(nickname);
    localStorage.setItem("inputRID",nickname);

}
window.addEventListener("load", function() {
                val = localStorage.getItem("inputRID");
                localStorage.removeItem("inputRID");
                document.getElementById("user_apply").value = val;
                document.getElementById("user_apply").innerHTML="Привет, "+val;
            })
function displayText() {
    nickname = document.getElementById("inputRID").value;
    console.log(nickname);
    localStorage.setItem("inputRID",nickname);

}
window.addEventListener("load", function() {
                val = localStorage.getItem("inputRID");
                localStorage.removeItem("inputRID");
                document.getElementById("input").value = val;
            })
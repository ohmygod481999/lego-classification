document.getElementById("submit-btn").addEventListener("click", function () {
    const files = document.getElementById("file").files;

    if (files.length === 0) return alert("vui long chon file");

    const formData = new FormData();

    formData.append("img", files[0]);

    fetch("/api/predict", {
        method: "POST",
        body: formData,
    }).then((res) => {
        res.json().then((json) => {
            const { success, predicts } = json;
            console.log(predicts);
            let str = "";
            predicts.forEach((pre, i) => {
                str += `${i + 1}.${predicts[i].label} - ${(
                    predicts[i].score * 100
                ).toFixed(2)}% \n`;
            });
            alert(
                success
                    ? `Tôi dự đoán là: \n${str}`
                    : "Noo, Upload fail"
            );
        });
    });
});

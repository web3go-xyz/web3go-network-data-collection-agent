let fs = require('fs');
let path = require('path');

let source_path = `/Users/zhangqixin/web3go_workspace/web3go_github/web3go-network-data-collection-agent/ApolloX-Doc/ApolloX_Finance/result`;

let target_file_path =`/Users/zhangqixin/web3go_workspace/web3go_github/web3go-network-data-collection-agent/ApolloX-Doc/ApolloX_Finance/full_docs_merged`
// let target_file =`${target_file_path}\\Litentry-Doc-en.txt`;
let target_file =`${target_file_path}/ApolloX-Finance-Doc-en-new.txt`;
function walkPathSync(currentDirPath, callback) {
    fs.readdirSync(currentDirPath, { withFileTypes: true }).forEach(function (dirent) {
        var filePath = path.join(currentDirPath, dirent.name);
        if (dirent.isFile()) {
            callback(filePath, dirent);
        } else if (dirent.isDirectory()) {
            walkSync(filePath, callback);
        }
    });
}
let all_texts = [];
walkPathSync(source_path, function (filePath, stat) {
    console.log(filePath);
    let text = fs.readFileSync(filePath, 'utf-8').toString()
    all_texts.push("Section: "+filePath.substring(filePath.lastIndexOf("/")+1, filePath.lastIndexOf(".txt"))+"\r\n"+text)
});


fs.writeFileSync(target_file, all_texts.join('\n\n'))
This script scrapes and stores the availability of timeslots for Car Driving Test at all RTA Serivce NSW centres in the state.
此脚本抓取并存储该州所有 RTA Service NSW 中心的汽车驾驶考试时间段的可用性。

## Dependencies 依赖

1. Account with RTA NSW where you can have passed knowledge test, hazard test etc.<br>
在新南威尔士州 RTA 的帐户中，您可以通过知识测试、危险测试等。

2. [chrome driver](https://sites.google.com/chromium.org/driver/) executable in your PATH variable.<br>
[chrome 驱动程序](https://sites.google.com/chromium.org/driver/)可执行文件在 PATH 变量中.

3. Python3 and Selenium installed.<br>
已安装 Python3 和 Selenium.

4. jq for json processing (for querying multiple locations and creating reports).<br>
用于 JSON 处理的 jq（用于查询多个位置和创建报告）

5. GNU parallel for querying availability for multiple locations.<br>
用于查询多个位置的可用性的 GNU parallel

## Usage 用法
#### Setting up the repo 设置存储库

Clone the repo
克隆存储库

git clone https://github.com/sbmkvp/rta_booking_information


Set your working directory to the repo
将工作目录设置为存储库

cd rta_booking_information


Copy and modify the sample settings file
复制和修改样本设置文件

cp settings_sample.json settings.json


Change the username, password to your own account. If you already have a booking in the system then set the `have_booking` variable to true. If you want to see the chromedriver UI then set the `headless` variable to false. The variables `wait_timer` and `wait_timer_car` can be increased to make the script suitable for slower internet connections. When the `git_upload` variable is set to true, the `get_all_locations.sh` script will try to commit the results back to github to update the website.
将用户名、密码更改为您自己的帐户。如果系统中已有预订，请将 `have_booking` 变量设置为 true。如果您想查看 chromedriver UI，请将 `headless` 变量设置为 false。变量 `wait_timer` 并且可以增加 `wait_timer_car` 以使脚本适合较慢的 Internet 连接。当 `git_upload` 变量设置为 true 时，`get_all_locations.sh` 脚本将尝试将结果提交回 GitHub 以更新网站。

#### Running the script for one location
为一个位置运行脚本

the scrape\_availability.py script takes two inputs - the id of the location and the file in which the result should be stored. The location ids are given in `docs/centers.json`. The output is a json file with an array of available timeslots and a variable showing the earliest timeslots.
scrape\_availability.py 脚本采用两个输入 - 位置的 ID 和 应存储结果的文件。位置 ID 在 `docs/centers.json` 中。输出是一个 json 文件，其中包含一组可用时隙和一个显示最早时隙的变量。

Run the script (for bash based systems e.g. mac/linux/WSL)
运行脚本（适用于基于 bash 的系统，例如 mac/linux/WSL）

./scrape_availability.py locationid file_to_save_results.json


Run the script (for windows)
运行脚本（适用于 Windows）

python3 scrape_availability.py locationid file_to_save_results.json


#### Running the script for multiple locations
为多个位置运行脚本

Availability for multiple locations could be scraped using the `get_all_locations.sh` script. Make sure there is a centers.json file in the docs folder with a list of centers you want to find availabilty for. This file is included in the repo but note that this changes regularly in the rta website so make sure you pull the latest file from the repo before running. Remove any files created during the last run (errors.txt, errors\_old.txt,results.json etc). The script when successful outputs results.json file in the docs folder and updates the `update-time.txt` file there.
可以使用 `get_all_locations.sh` 抓取多个位置的可用性 脚本。确保 docs 文件夹中有一个 centers.json 文件，其中包含 您想要找到可用性的中心。此文件包含在存储库中，但请注意 这在 RTA 网站中会定期更改，因此请确保您提取最新的 文件。删除在上次 run（errors.txt、errors\_old.txt、results.json 等）。成功输出时的脚本 results.json docs 文件夹中的文件，并在其中更新 `update-time.txt` 文件。

./get_all_locations.sh


Once completed, the results could be viewed at [http://localhost:8888](http://localhost:8888) after running a simple http server at the docs folder by running,
完成后，在 docs 文件夹中运行一个简单的 http 服务器后，可以通过运行 [http://localhost:8888](http://localhost:8888) 查看结果，

python3 -m http.server 8888


This script and the one below works only in systems with POSIX compliant shell. For windows, please use a POSIX compliant shell like [git-bash](https://gitforwindows.org/) or [cygwin](http://cygwin.com/). We also need to install [jq](https://stackoverflow.com/questions/52393850/how-to-install-gnu-parallel-on-windows-10-using-git-bash) and [parallel](https://stackoverflow.com/questions/53967693/how-to-run-jq-from-gitbash-in-windows) for windows. You can also use [WSL](https://docs.microsoft.com/en-us/windows/wsl/install) and create a full linux environment inside windows.
此脚本和下面的脚本仅适用于具有 POSIX 兼容 shell 的系统。对于 Windows，请使用符合 POSIX 的 shell，例如 [git-bash](https://gitforwindows.org/) 或 [Cygwin](http://cygwin.com/)。我们还需要安装 [JQ](https://stackoverflow.com/questions/52393850/how-to-install-gnu-parallel-on-windows-10-using-git-bash) 和 [Parallel（适用于](https://stackoverflow.com/questions/53967693/how-to-run-jq-from-gitbash-in-windows) Windows）。您还可以使用 [WSL](https://docs.microsoft.com/en-us/windows/wsl/install) 并在 Windows 中创建完整的 linux 环境。

#### Create a csv report
创建 csv 报告

Alternatively you can convert the results stored in the docs folder into a csv by using the `create_status_report` script.
或者，您也可以使用 `create_status_report` 脚本将存储在 docs 文件夹中的结果转换为 csv。

./create_status_report docs/centers.json docs/results.json


### Containerised implementation
容器化实施

The containerised implementation can be used to run this script on the cloud at regular intervals. If you want to host a github site with the results, please change the repo address in dockerfile to yours and then create the gitconfig and git-credential files from the samples provided. Then build the continer by doing,
容器化实现可用于定期在云上运行此脚本。如果要托管包含结果的 github 站点，请将 dockerfile 中的存储库地址更改为您的地址，然后根据提供的示例创建 gitconfig 和 git-credential 文件。然后通过执行

docker build -t rta_booking_availability .


Once the image has been built you can run the container with regular update interval by,
构建映像后，您可以通过以下方式以定期更新间隔运行容器：

docker run --restart unless-stopped --name rta_booking_availability -d rta_booking_availability


If your want to add a delay of n seconds between subsequent updates, add `sleep(n)` to the end of get\_all\_locations.shscript.
如果要在后续更新之间添加 n 秒的延迟，请将 `sleep（n）` 添加到 get\_all\_locations.shscript 的末尾。

### Note
注意

This has been tested to work in my system but there are numerous edge cases where this might fail.
这已经在我的系统中进行了测试，但在许多极端情况下可能会失败。

*   Your account status is different to mine
您的帐户状态与我的不同
*   RTA changes website.
RTA 更改网站。
*   RTA IT team blocks your IP
RTA IT 团队阻止您的 IP
*   The website is very slow
网站速度很慢

If the website is slow and the script fails at selecting the driving test on a new booking try increasing the wait\_timer.
如果网站运行缓慢，并且脚本无法在新预订中选择驾驶考试，请尝试增加 wait\_timer。

## Disclaimer 免责声明：

*   For personal use only.
仅供个人使用。
*   Dont break the law or cause disruption using this.
不要利用这个触犯法律或造成破坏。
*   Using automated scripts irresponsibily can cause booking loss, disruption of services etc. be careful and know what you are doing.
不负责任地使用自动化脚本可能会导致预订丢失、服务中断等。要小心并知道你在做什么。
*   You are responsible for your actions.
你要对自己的行为负责。

## Update info 更新信息：

*   更新了识别Safari和Chrome的代码，在`Setting.json`文件里面的`browser`修改参数，`1=Chrome, 0=Safari`。
更新了识别 Safari 和 Chrome 的代码，在 `Setting.json` 文件里面的`浏览器`修改参数，`1=Chrome， 0=Safari`。

# Contact me 联系开发者：
[联系开发者并且向他发送一个BUG](mailto:noreply@visionstudio.asia?subject=ReportBUG)




# 开发者代办区：
1. 更新了www.myrta.com的网址，适用于没有账户密码的用户使用Family Name和Customer Number登录。（2025-03-30）（✅）
2. 增加了浏览器的判断，使适配Safari和Chrome。（2025-03-30）（✅）
3. 需要在MD里面添加MyRTA仅适用于英文系统。（2025-03-30）（❌）
4. 对于使用Safari的用户，需要让他们开启Safari的`开发者模式`以及`自动控制`。（2025-03-30）（❌）
5. 关于用户网络环境造成页面延时，过慢的网络环境会导致`time.sleep(&)`超时。是否需要添加手动可调延时？（2025-03-30）（❌）
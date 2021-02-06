# Dedeler-Roket-Takimi
Teknofest2021 roket  iki kademe atış hazırlıkarı

Kurulumlar

Dronekit kurulumu
sudo apt-get install python-dev
Pip install dronekit


Gstreamer kurulumu
sudo apt-get install gstreamer1.0-tools gstreamer1.0-plugins-good gstreamer1.0-plugins-bad



Ubuntu bilgisayarda 
gst-launch-1.0 -v udpsrc port=9000 caps='application/x-rtp, media=(string)video, clock-rate=(int)90000, encoding-name=(string)H264' ! rtph264depay ! avdec_h264 ! videoconvert ! autovideosink sync=f
bu kod parçası calıştırılacak
Raspberry de bu kod(<remote_ip> kısmını sil ve görüntünün gönderileceği bilgisayarın ip adresini yaz)
raspivid -n -w 1280 -h 720 -b 1000000 -fps 15 -t 0 -o - | gst-launch-1.0 -v fdsrc ! h264parse ! rtph264pay config-interval=10 pt=96 ! udpsink host=<remote_ip> port=9000




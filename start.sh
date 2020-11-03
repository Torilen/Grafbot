pip uninstall -y googletrans 
cd ../py-googletrans 
echo "y" | python setup.py install
cd ../Grafbot
git pull
python app/webapp.py -t blended_skill_talk -mf zoo:blender/blender_90M/model


#!/bin/bash
#prompt user if they want to discard changes
echo "Do you want to discard changes? (y/n)"
read discard_changes
if [ "$discard_changes" == "y" ]; then
    echo "Discarding changes..."
    git reset --hard HEAD
else
    echo "Keeping changes..."
fi
#prompt user if they want to pull changes
echo "Do you want to pull changes? (y/n)"
read pull_changes
if [ "$pull_changes" == "y" ]; then
    echo "Pulling changes..."
else
    echo "Skipping pull..."
fi
#pull changes from remote repository    
git pull https://github.com/Ruben-van-Breda/my-assistant.git
from SnapshortAgent import SnapshortAgent

def main():
    print "working"
    tools=SnapshortAgent()
    print "working 2"
    savedImage=tools.takeSnapshot()
    tools.saveSnapshot(savedImage, 'tempPic')
    print "working 3"
    print tools.compareSnapshots(savedImage, savedImage)
    print "working 4"
    print tools.compareSnapshots(savedImage, tools.loadSnapshot('screen_shot2.png'))
    print "working 5"
    print tools.takeAndCompareSnapshots(tools.loadSnapshot('screen_shot2.png'))
    print "working 6"
if __name__ == "__main__":
    main()
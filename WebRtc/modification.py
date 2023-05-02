class VideoTransformTrack(VideoStreamTrack):
    def __init__(self, transform):
        super().__init__()
        self.transform = transform

    async def recv(self):
        frame = await self.next_timestamp()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = self.transform(frame)
        return frame

async def offer_video(pc, video_file):
    # Read video file
    cap = cv2.VideoCapture(video_file)
    if not cap.isOpened():
        print("Error opening video file")
        return

    # Create video stream track
    transform = lambda img: cv2.resize(img, (640, 480))
    track = VideoTransformTrack(transform)

    # Add video stream to peer connection
    pc.addTrack(track)

    # Start streaming video
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        await track.put(frame)

    cap.release()

async def run():
    # Create WebRTC peer connection
    pc = RTCPeerConnection()

    # Offer video
    video_file = "input_video.mp4"
    await offer_video(pc, video_file)

    # Get local description and print it
    desc = await pc.createOffer()
    await pc.setLocalDescription(desc)
    print(pc.localDescription.sdp)

    # Wait for ICE gathering to complete
    await pc.gatherCandidates()

module Demo
{
    sequence<byte> Bytes;

    class StreamingInfo
    {
        string url;
        string clientIP;
        long duration;
    }


    interface Printer
    {
        StreamingInfo playMusic(string s);
        string getSongList();
        string getSearchByTitle(string title);
        string getSearchByAuthor(string author);
        void changeSongTitle(string title, string newTitle);
        void changeSongAuthor(string title, string newAuthor);
        void deleteSong(string title);
        void stopMusic();
        void playPauseMusic();
    }

    interface FileTransfer {
        void sendFile(Bytes data, string title);
    };
}
module Demo
{
    sequence<byte> Bytes;


    interface Printer
    {
        string playMusic(string s);
        string getSongList();
        string getSearchByTitle(string title);
        string getSearchByAuthor(string author);
        void changeSongTitle(string title, string newTitle);
        void changeSongAuthor(string title, string newAuthor);
        void deleteSong(string title);
    }

    interface FileTransfer {
        void sendFile(Bytes data, string title);
    };
}
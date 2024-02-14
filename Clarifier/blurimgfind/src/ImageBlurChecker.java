import org.opencv.core.*;
import org.opencv.imgcodecs.Imgcodecs;
import org.opencv.imgproc.Imgproc;

import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import java.io.File;
import java.util.*;
import java.util.List;

import static org.opencv.core.CvType.CV_8U;

public class ImageBlurChecker extends JFrame {
    private static final long serialVersionUID = 1L;

    private JTextArea logTextArea;
    private JFileChooser fileChooser;
    private File selectedFolder;
    private File blurFolder;

    public ImageBlurChecker() {
        setTitle("Image Blur Checker");
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setSize(500, 300);

        logTextArea = new JTextArea();
        logTextArea.setEditable(false);

        fileChooser = new JFileChooser();
        fileChooser.setFileSelectionMode(JFileChooser.DIRECTORIES_ONLY);

        JButton selectFolderButton = new JButton("Select Folder");
        selectFolderButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                int result = fileChooser.showOpenDialog(ImageBlurChecker.this);
                if (result == JFileChooser.APPROVE_OPTION) {
                    selectedFolder = fileChooser.getSelectedFile();
                    logTextArea.append("Selected Folder: " + selectedFolder.getName() + "\n");

                    blurFolder = new File(selectedFolder.getAbsolutePath() + File.separator + "BlurImages");
                    blurFolder.mkdir();

                    processImages();
                }
            }
        });

        JPanel buttonPanel = new JPanel(new FlowLayout());
        buttonPanel.add(selectFolderButton);

        JScrollPane logScrollPane = new JScrollPane(logTextArea);

        setLayout(new BorderLayout());
        add(buttonPanel, BorderLayout.NORTH);
        add(logScrollPane, BorderLayout.CENTER);
    }

    private void processImages() {
        logTextArea.append("Processing images...\n");

        File[] imageFiles = selectedFolder.listFiles((dir, name) -> name.toLowerCase().endsWith(".jpg") || name.toLowerCase().endsWith(".png"));

        if (imageFiles != null) {
            for (File imageFile : imageFiles) {
                if (isImageBlurry(imageFile)) {
                    moveImageToBlurFolder(imageFile);
                }
            }
        }

        logTextArea.append("Image processing complete.\n");
    }

    private boolean isImageBlurry(File imageFile) {
        logTextArea.append("Checking blur for: " + imageFile.getName() + "\n");

        Mat image = Imgcodecs.imread(imageFile.getAbsolutePath());
        Mat grayImage = new Mat();
        Imgproc.cvtColor(image, grayImage, Imgproc.COLOR_BGR2GRAY);

        Mat laplacianImage = new Mat();
        Imgproc.Laplacian(grayImage, laplacianImage, CV_8U);

        MatOfFloat histogram = new MatOfFloat();
        MatOfInt histSize = new MatOfInt(256);
        MatOfInt channels = new MatOfInt(0);

        List<Mat> images = new ArrayList<>();
        images.add(laplacianImage);
        Imgproc.calcHist(images, channels, new Mat(), histogram, histSize, new MatOfFloat(0, 256));

        double sum = 0;
        for (int i = 0; i < histogram.rows(); i++) {
            sum += (i * histogram.get(i, 0)[0]);
        }

        double mean = sum / image.total();
        double variance = 0;
        for (int i = 0; i < histogram.rows(); i++) {
            variance += ((i - mean) * (i - mean) * histogram.get(i, 0)[0]);
        }

        double blur = variance / image.total();

        logTextArea.append("Blur Value: " + blur + "\n");

        return blur > 1000; // Adjust the threshold based on your requirements
    }

    private void moveImageToBlurFolder(File imageFile) {
        logTextArea.append("Moving blurry image: " + imageFile.getName() + "\n");

        File destinationFile = new File(blurFolder.getAbsolutePath() + File.separator + imageFile.getName());
        imageFile.renameTo(destinationFile);
    }

    public static void main(String[] args) {
        System.loadLibrary(org.opencv.core.Core.NATIVE_LIBRARY_NAME);

        SwingUtilities.invokeLater(new Runnable() {
            @Override
            public void run() {
                new ImageBlurChecker().setVisible(true);
            }
        });
    }
}

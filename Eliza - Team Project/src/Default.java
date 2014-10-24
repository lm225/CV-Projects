import java.io.*;
import java.util.Random;
public class Default {

	//method to provide a default response when necessary
	public boolean defaultResponses() throws IOException{

		try{
			BufferedReader reader = new BufferedReader(new FileReader("script.txt"));
			String response;

			//read each line of the script (to the end)
			while((response = reader.readLine()) != null){
				//array to contain the words of each line in the script
				String[] defaultArray = response.split("::");
				//check that the first character of the line is a 5
				if (response.charAt(0) == ('5')) {

					//generate a random number to give a random response
					int r = 0;
					while(r < 2){
						Random random = new Random();
						r = random.nextInt(defaultArray.length);
					}
					System.out.println(defaultArray[r]);




				}
			}
			//create a new Eliza object and recall the start method
			Eliza e = new Eliza();
			e.start();

		}

		catch(FileNotFoundException e){
			System.out.println("The File Specified Could Not Be Found");


		}return true;

	}
}
